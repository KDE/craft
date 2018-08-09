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

    def _setDefaults(self, defines):
        defines = dict(defines)
        defines.setdefault("company", "KDE")
        defines.setdefault("name", self.package.name)
        defines.setdefault("display_name", self.subinfo.displayName)
        defines.setdefault("description", self.subinfo.description)
        defines.setdefault("executable", self.defines["shortcuts"][0]["target"])
        defines.setdefault("icon_png", os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craft.ico"))
        defines.setdefault("setupname", os.path.join(self.packageDestinationDir(), self.binaryArchiveName(fileType="appx", includeRevision=True)))
        defines.setdefault("publisher", f"CN={CraftCore.settings.get('CodeSigning', 'CommonName')}, "
                                        f"O={CraftCore.settings.get('CodeSigning', 'Organization')}, "
                                        f"L={CraftCore.settings.get('CodeSigning', 'Locality')}, "
                                        f"C={CraftCore.settings.get('CodeSigning', 'Country')}")
        version = str(CraftVersion(self.version).strictVersion)
        if version.count(".") < 4:
            version = f"{version}.0"
        defines.setdefault("version", version)
        return defines


    def createPackage(self):
        defines = self._setDefaults(self.defines)
        archive = defines["setupname"]
        if os.path.isfile(archive):
            utils.deleteFile(archive)
        return (self.internalCreatePackage() and
                utils.copyFile(os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craftyBENDER.png"),
                               os.path.join(self.archiveDir(), "craftyBENDER.png")) and
                utils.configureFile(os.path.join(os.path.dirname(__file__), "AppxManifest.xml"), os.path.join(self.archiveDir(), "AppxManifest.xml"), defines) and
                utils.system(["makeappx", "pack", "/d", self.archiveDir(), "/p", defines["setupname"]]) and
                utils.sign([defines["setupname"]]))
