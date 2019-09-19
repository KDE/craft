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


from Utils import CraftHash
from Packager.CollectionPackagerBase import *
from Packager.PortablePackager import *
from Blueprints.CraftVersion import CraftVersion


class AppxPackager(CollectionPackagerBase):
    Extensions = r"""
        <uap:Extension Category="windows.fileTypeAssociation">
          <uap:FileTypeAssociation Name="@{craft_id}">
            <uap:SupportedFileTypes>
              @{file_types}
            </uap:SupportedFileTypes>
          </uap:FileTypeAssociation>
        </uap:Extension>"""

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
            defines["file_types"] = "\n".join([f"""<uap:FileType>{t}</uap:FileType>""" for t in set(defines["file_types"])])
            defines.setdefault("extensions", AppxPackager.Extensions)
        else:
            defines.setdefault("file_types", "")
            defines.setdefault("extensions", "")



    def setDefaults(self, defines : dict) -> dict:
        defines = super().setDefaults(defines)
        version = str(CraftVersion(defines.get("version", self.version)).normalizedVersion)
        # we require a version of the format 1.2.3.4
        count = version.count(".")
        if count < 4:
            version = f"{version}{'.0' * (3-count)}"
        defines["version"] = version + self.buildNumber()

        defines.setdefault("name", f"{defines['company']}{defines['display_name']}".replace(" ", ""))

        utils.createDir(self.artifactsDir())
        defines["setupname"] = self.artifactsDir() / os.path.basename(f"{defines['setupname']}.appx")
        defines.setdefault("craft_id", self.package.path.replace("/", "."))

        self._setupFileTypes(defines)

        if (Path(self.archiveDir()) /"bin/snoretoast.exe").exists():
            defines["extensions"] += AppxPackager.SnoreToast
        if "startup_task" in defines:
            defines["extensions"] += AppxPackager.StartUp

        extensions = defines["extensions"]
        if extensions:
            defines["extensions"] = f"<Extensions>{extensions}</Extensions>"

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
        appendToPublisherString(publisher, "L", "Locality")
        appendToPublisherString(publisher, "S", "State")
        appendToPublisherString(publisher, "C", "Country")
        defines["publisher"] = ", ".join(publisher)
        setupName = os.path.join(self.packageDestinationDir(), "{0}-sideload{1}".format(*os.path.splitext(os.path.basename(defines["setupname"]))))
        defines["setupname"] =  setupName
        return self.__createAppX(defines) and utils.sign([setupName])

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

