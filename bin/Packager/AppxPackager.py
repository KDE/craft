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

from Utils import CraftHash
from Packager.CollectionPackagerBase import *
from Packager.PortablePackager import *
from Blueprints.CraftVersion import CraftVersion


class AppxPackager(CollectionPackagerBase):

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    @staticmethod
    def _appendToPublisherString(publisher : [str], field : str, key : str ) -> None:
        data = CraftCore.settings.get("CodeSigning", key, "")
        if data:
            publisher += [f"{field}={data}" ]

    def _setDefaults(self, defines : dict) -> dict:
        defines = dict(defines)
        if "version" not in defines:
            version = str(CraftVersion(self.version).strictVersion)
            # we require a version of the format 1.2.3.4
            count = version.count(".")
            if count < 4:
                version = f"{version}{'.0' * (3-count)}"
            defines.setdefault("version", version)

        defines.setdefault("company", "KDE")
        defines.setdefault("name", self.package.path.replace("/", "."))
        defines.setdefault("id", defines["name"].replace("-", "."))
        defines.setdefault("display_name", self.subinfo.displayName)
        defines.setdefault("description", self.subinfo.description)
        defines.setdefault("icon_png", os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craftyBENDER.png"))
        defines.setdefault("icon_png_44", defines["icon_png"])
        defines.setdefault("setupname", os.path.join(self.packageDestinationDir(), self.binaryArchiveName(fileType="appx", includeRevision=True)))

        # compat with nsis
        if "shortcuts" in self.defines:
            defines.setdefault("executable", self.defines["shortcuts"][0]["target"])

        publisher = []
        self._appendToPublisherString(publisher, "CN", "CommonName")
        self._appendToPublisherString(publisher, "O", "Organization")
        self._appendToPublisherString(publisher, "L", "Locality")
        self._appendToPublisherString(publisher, "C", "Country")
        self._appendToPublisherString(publisher, "S", "State")
        defines.setdefault("publisher", ", ".join(publisher))

        return defines


    def createPackage(self):
        defines = self._setDefaults(self.defines)
        archive = defines["setupname"]

        if os.path.isfile(archive):
            utils.deleteFile(archive)

        if not "executable" in defines:
            CraftCore.log.error("Please add self.defines['shortcuts'] to the installer defines. e.g.\n"
                                """self.defines["shortcuts"] = [{"name" : "Kate", "target":"bin/kate.exe", "description" : self.subinfo.description}]""")
            return False

        if not self.internalCreatePackage():
            return False

        icon = defines["icon_png"]
        icon_44 = defines["icon_png_44"]
        defines["icon_png"] = os.path.basename(icon)
        defines["icon_png_44"] = os.path.basename(icon_44)

        if not utils.copyFile(icon, os.path.join(self.archiveDir(), defines["icon_png"])):
            return False
        if icon != icon_44:
            if not utils.copyFile(icon_44, os.path.join(self.archiveDir(), defines["icon_png_44"])):
                return False
        return (utils.configureFile(os.path.join(os.path.dirname(__file__), "AppxManifest.xml"), os.path.join(self.archiveDir(), "AppxManifest.xml"), defines) and
                utils.system(["makeappx", "pack", "/d", self.archiveDir(), "/p", defines["setupname"]]) and
                utils.sign([defines["setupname"]]))
