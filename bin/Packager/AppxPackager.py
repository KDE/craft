# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import os
import mimetypes


from Utils import CraftHash, CodeSign
from Packager.CollectionPackagerBase import *
from Packager.PortablePackager import *
from Blueprints.CraftVersion import CraftVersion


class AppxPackager(CollectionPackagerBase):
    XMLNamespaces = r"""
    xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
         xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
         xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
         xmlns:mp="http://schemas.microsoft.com/appx/2014/phone/manifest"
         xmlns:com="http://schemas.microsoft.com/appx/manifest/com/windows10"
         xmlns:desktop="http://schemas.microsoft.com/appx/manifest/desktop/windows10"
         xmlns:uap10="http://schemas.microsoft.com/appx/manifest/uap/windows10/10"
         @{additional_xmlns}
    """
    Extensions = r"""
        <uap:Extension Category="windows.fileTypeAssociation">
          <uap:FileTypeAssociation Name="@{craft_id}">
            <uap:SupportedFileTypes>
              @{file_types}
            </uap:SupportedFileTypes>
          </uap:FileTypeAssociation>
        </uap:Extension>"""

    Capabilities = r"""
        <rescap:Capability Name="runFullTrust" />
        @{additional_capabilities}
    """

    StartUp = r"""
        <desktop:Extension Category="windows.startupTask" Executable="@{startup_task}" EntryPoint="Windows.FullTrustApplication">
          <desktop:StartupTask TaskId="@{craft_id}" Enabled="true" DisplayName="@{display_name}" />
        </desktop:Extension>"""

    # https://docs.microsoft.com/en-us/windows/uwp/design/shell/tiles-and-notifications/send-local-toast-desktop
    # TODO: get the correct CLSID from snoretoast
    SnoreToast = r"""
        <!--Register COM CLSID LocalServer32 registry key-->
        <com:Extension Category="windows.comServer">
          <com:ComServer>
            <com:ExeServer Executable="bin\snoretoast.exe" DisplayName="SnoreToast activator">
              <com:Class Id="eb1fdd5b-8f70-4b5a-b230-998a2dc19303" DisplayName="Toast activator"/>
            </com:ExeServer>
          </com:ComServer>
        </com:Extension>

        <!--Specify which CLSID to activate when toast clicked-->
        <desktop:Extension Category="windows.toastNotificationActivation">
          <desktop:ToastNotificationActivation ToastActivatorCLSID="eb1fdd5b-8f70-4b5a-b230-998a2dc19303" />
        </desktop:Extension>"""

    Aliases = r"""<uap3:Extension Category="windows.appExecutionAlias" Executable="@{alias_executable}" EntryPoint="Windows.FullTrustApplication">
          <uap3:AppExecutionAlias>
            <desktop:ExecutionAlias Alias="@{alias}" />
          </uap3:AppExecutionAlias>
          </uap3:Extension>"""

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    @staticmethod
    def _setupFileTypes(defines):
        if "mimetypes" in defines:
            defines["file_types"] = set(defines.get("file_types", set()))
            mimetypes.init()
            for t in defines["mimetypes"]:
                types = set(mimetypes.guess_all_extensions(t))
                if not types:
                    raise Exception(f"Unsupported mime type {t}")
                defines["file_types"].update(types)
            # remove reserved associations (packaging woud fail)
            defines["file_types"] -= {".bat", ".com", ".exe"}
            del defines["mimetypes"]

        if "file_types" in defines:
            CraftCore.log.info("The package will support the following file types:")
            CraftCore.log.info(defines["file_types"])
            defines["file_types"] = "\n".join([f"""<uap:FileType>{t}</uap:FileType>""" if t != "*" else f"""<uap10:FileType>{t}</uap10:FileType>""" for t in set(defines["file_types"])])
            defines.setdefault("extensions", AppxPackager.Extensions)
        else:
            defines.setdefault("file_types", "")
            defines.setdefault("extensions", "")



    def setDefaults(self, defines : dict) -> dict:
        defines = super().setDefaults(defines)
        defines.setdefault("additional_xmlns", "")
        version = [int(x) for x in CraftVersion(defines.get("version", self.version)).normalizedVersion.versionstr.split(".")]
        # we require a version of the format 1.2.3.4
        version += [0] * (4-len(version))
        version[1] = version[1] * 100 + version[2]
        if self.buildNumber():
            version[2] = self.buildNumber()
        else:
            version[2] = 0
        # part 4 must be 0 for the store
        # we ignore the patch level, build number ensures increasing version numbers
        version[3] = 0
        defines["version"] = ".".join([str(x) for x in version])

        defines.setdefault("name", f"{defines['company']}{defines['display_name']}".replace(" ", ""))

        utils.createDir(self.artifactsDir())
        defines["setupname"] = self.artifactsDir() / os.path.basename(f"{defines['setupname']}.appx")
        defines.setdefault("craft_id", self.package.path.replace("/", "."))

        self._setupFileTypes(defines)

        if "dev-utils/snoretoast" in CraftDependencyPackage(self.package).getDependencies(DependencyType.Runtime):
            defines["extensions"] += AppxPackager.SnoreToast
        if "startup_task" in defines:
            defines["extensions"] += AppxPackager.StartUp

        if "alias" in defines:
            if not defines["alias"].endswith(CraftCore.compiler.executableSuffix):
                defines["alias"] += CraftCore.compiler.executableSuffix
            defines["extensions"] += AppxPackager.Aliases
            defines["additional_xmlns"] += """xmlns:uap3="http://schemas.microsoft.com/appx/manifest/uap/windows10/3"\n"""
            defines.setdefault("alias_executable", self.defines["executable"] if "executable" in self.defines else self.defines["shortcuts"][0]["target"])

        extensions = defines["extensions"]
        if extensions:
            defines["extensions"] = f"<Extensions>{extensions}</Extensions>"

        defines.setdefault("additional_capabilities", "")

        defines.setdefault("capabilities", AppxPackager.Capabilities)
        capabilities = defines["capabilities"]

        if capabilities:
            defines["capabilities"] = f"<Capabilities>{capabilities}</Capabilities>"

        defines.setdefault("desktop_extensions", "")
        desktop_extensions = defines["desktop_extensions"]

        if desktop_extensions:
            defines["desktop_extensions"] = f"<Extensions>{desktop_extensions}</Extensions>"

        defines.setdefault("xml_namespaces", AppxPackager.XMLNamespaces)
        xml_namespaces = defines["xml_namespaces"]

        if xml_namespaces:
            defines["xml_namespaces"] = f"{xml_namespaces}"

        # compat with nsis
        if "shortcuts" in self.defines:
            defines.setdefault("executable", self.defines["shortcuts"][0]["target"])
        return defines

    def __prepareIcons(self, defines):
        utils.createDir(os.path.join(self.archiveDir(), "Assets"))
        defines["logo"] = os.path.join('Assets', os.path.basename(defines["icon_png"]))
        for propertyName, define, required in [ ("Square150x150Logo", "icon_png", True),
                                                ("Square44x44Logo", "icon_png_44", True),
                                                ("Wide310x150Logo", "icon_png_310x150", False),
                                                ("Square310x310Logo", "icon_png_310x310", False),
                                                ]:
            if define not in defines:
                if required:
                    CraftCore.log.info(f"Please add defines[\"{define}]\"")
                    return False
                else:
                  defines[define] = ""
                  continue

            icon = defines[define]
            defines[define] = f"{propertyName}=\"{os.path.join('Assets', os.path.basename(icon))}\""
            names = glob.glob("{0}*{1}".format(*os.path.splitext(icon)))
            if not names:
                CraftCore.log.error(f"Failed to find {icon}")
                return False
            for n in names:
                if not utils.copyFile(n, os.path.join(self.archiveDir(), "Assets", os.path.basename(n))):
                    return False
        return True

    def __createAppX(self, defines) -> bool:
        archive = defines["setupname"]
        if os.path.isfile(archive):
            utils.deleteFile(archive)
        return (utils.configureFile(os.path.join(os.path.dirname(__file__), "AppxManifest.xml"), os.path.join(self.archiveDir(), "AppxManifest.xml"), defines) and
                utils.system(["makeappx", "pack", "/d", self.archiveDir(), "/p", archive]))

    def __createSideloadAppX(self, defines) -> bool:
        def appendToPublisherString(publisher: [str], field: str, key: str) -> None:
            data = CraftCore.settings.get("CodeSigning", key, "")
            if data:
                publisher += [f"{field}={data}"]

        publisher = []
        appendToPublisherString(publisher, "CN", "CommonName")
        appendToPublisherString(publisher, "O", "Organization")
        appendToPublisherString(publisher, "STREET", "Street")
        appendToPublisherString(publisher, "L", "Locality")
        appendToPublisherString(publisher, "S", "State")
        appendToPublisherString(publisher, "PostalCode", "PostalCode")
        appendToPublisherString(publisher, "C", "Country")
        defines["publisher"] = ", ".join(publisher)
        setupName = os.path.join(self.packageDestinationDir(), "{0}-sideload{1}".format(*os.path.splitext(os.path.basename(defines["setupname"]))))
        defines["setupname"] =  setupName
        return self.__createAppX(defines) and CodeSign.signWindows([setupName])

    def createPackage(self):
        defines = self.setDefaults(self.defines)

        if not "executable" in defines:
            CraftCore.log.error("Please add self.defines['shortcuts'] to the installer defines. e.g.\n"
                                """self.defines["shortcuts"] = [{"name" : "Kate", "target":"bin/kate.exe", "description" : self.subinfo.description}]""")
            return False
        publisherId = CraftCore.settings.get("Packager", "AppxPublisherId", "")
        createStorePackage = bool(publisherId)
        utils.cleanDirectory(self.artifactsDir())
        if not self.internalCreatePackage(defines, seperateSymbolFiles=createStorePackage, packageSymbols=False):
            return False

        if not self.__prepareIcons(defines):
            return False

        if createStorePackage:
            defines.setdefault("publisher", publisherId)
            if not self.__createAppX(defines):
                return False
            appxSym = Path(defines["setupname"]).with_suffix(".appxsym")
            if appxSym.exists():
                appxSym.unlink()
            if not utils.compress(appxSym, self.archiveDebugDir()):
                return False
            appxUpload = (Path(self.packageDestinationDir()) / os.path.basename(defines["setupname"])).with_suffix(".appxupload")
            if appxUpload.exists():
                appxUpload.unlink()
            if not utils.compress(appxUpload, self.artifactsDir()):
                return False

        return self.__createSideloadAppX(defines)

