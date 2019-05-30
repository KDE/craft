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
    Extensions = f"""<Extensions>
        <uap:Extension Category="windows.fileTypeAssociation">
          <uap:FileTypeAssociation Name="@{{craft_id}}">
            <uap:SupportedFileTypes>
              @{{file_types}}
            </uap:SupportedFileTypes>
          </uap:FileTypeAssociation>
        </uap:Extension>
      </Extensions>"""

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    @staticmethod
    def _setupFileTypes(defines):
        if "mimetypes" in defines:
            defines.setdefault("file_types", set())
            mimetypes.init()
            for t in defines["mimetypes"]:
                types = set(mimetypes.guess_all_extensions(t))
                #remove reserved associations
                types -= {".bat", ".com", ".exe"}
                defines["file_types"] += types
            del defines["mimetypes"]

        if "file_types" in defines:
            defines["file_types"] = "\n".join([f"""<uap:FileType>{t}</uap:FileType>""" for t in set(defines["file_types"])])
            defines.setdefault("extensions", AppxPackager.Extensions)
        else:
            defines.setdefault("file_types", "")
            defines.setdefault("extensions", "")


    def setDefaults(self, defines : dict) -> dict:
        defines = super().setDefaults(defines)
        version = str(CraftVersion(defines.get("version", self.version)).strictVersion)
        # we require a version of the format 1.2.3.4
        count = version.count(".")
        if count < 4:
            version = f"{version}{'.0' * (3-count)}"
        defines["version"] = version

        defines.setdefault("name", f"{defines['company']}{defines['display_name']}".replace(" ", ""))
        defines.setdefault("setupname", os.path.join(self.packageDestinationDir(), self.binaryArchiveName(fileType="appx", includeRevision=True)))
        defines.setdefault("craft_id", self.package.path.replace("/", "."))

        self._setupFileTypes(defines)
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
        setupName = "{0}-sideload{1}".format(*os.path.splitext(defines["setupname"]))
        defines["setupname"] = setupName
        return self.__createAppX(defines) and utils.sign([setupName])

    def createPackage(self):
        defines = self.setDefaults(self.defines)

        if not "executable" in defines:
            CraftCore.log.error("Please add self.defines['shortcuts'] to the installer defines. e.g.\n"
                                """self.defines["shortcuts"] = [{"name" : "Kate", "target":"bin/kate.exe", "description" : self.subinfo.description}]""")
            return False

        if not self.internalCreatePackage():
            return False

        if not self.__prepareIcons(defines):
            return False

        publisher = CraftCore.settings.get("Packager", "AppxPublisherId", "")
        if publisher:
            defines.setdefault("publisher", publisher)
            if not self.__createAppX(defines):
                return False

        return self.__createSideloadAppX(defines)

