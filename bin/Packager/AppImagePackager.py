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
from .CollectionPackagerBase import *
from .SevenZipPackager import *
from .NullsoftInstallerPackager import *

class AppImagePackager(CollectionPackagerBase):
    """
Packager for portal 7zip archives
"""

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def _setDefaults(self):
        # TODO: Fix defaults
        self.defines.setdefault("apppath", "")
        self.defines.setdefault("appname", self.package.name.lower())

    def createPackage(self):
        """ create a package """

        if 1:
            if not self.internalCreatePackage():
                return False
            utils.mergeTree(self.archiveDir(), os.path.join(self.archiveDir(), "usr"))

        self._setDefaults()
        # TODO: "--plugin=checkrt"
        return utils.system(["linuxdeploy", "--appdir", self.archiveDir(), "--executable", os.path.join(self.archiveDir(), "usr", "bin", self.defines['appname']),
                             #"--desktop-file", os.path.join(self.archiveDir(), "usr", "share", "applications" ,"org.kde.kate.desktop"),
                             "--create-desktop-file",
                             "--icon-file",  os.path.join(CraftCore.standardDirs.craftRoot(), "share", "icons", "hicolor", "64x64", "apps", "kate.png"),
                             "-v", "0",
                             "--output=appimage"])
