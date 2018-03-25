# -*- coding: utf-8 -*-
# Copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
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

#
# creates a 7z archive from the whole content of the package image
# directory or optional from a sub directory of the image directory

# This packager is in an experimental state - the implementation
# and features may change in further versions

import json
import subprocess

from Packager.PackagerBase import *
from Utils import CraftHash
from CraftOS.osutils import OsUtils

class SevenZipPackager(PackagerBase):
    """Packager using the 7za command line tool from the dev-utils/7zip package"""

    @InitGuard.init_once
    def __init__(self):
        PackagerBase.__init__(self)

    def __7z(self, archive, sourceDir):
        app = CraftCore.cache.findApplication("7za")
        kw = {}
        progressFlags = []
        if CraftCore.cache.checkCommandOutputFor(app, "-bs"):
            progressFlags = ["-bso2", "-bsp1"]
            kw["stderr"] = subprocess.PIPE
        cmd = [app, "a", "-r",  archive, os.path.join(sourceDir, "*")] + progressFlags
        return utils.system(cmd, displayProgress=True, **kw)

    def __xz(self, archive, sourceDir):
        return utils.system(["tar", "-cJf", archive, "-C", sourceDir, ".",])

    def _compress(self, archiveName, sourceDir, destDir, createDigests=True) -> bool:
        archive = os.path.join(destDir, archiveName)
        utils.createDir(os.path.dirname(archive))
        if os.path.isfile(archive):
            utils.deleteFile(archive)
        if OsUtils.isUnix():
            if not self.__xz(archive, sourceDir):
                return False
        else:
            if not self.__7z(archive, sourceDir):
                return False

        if createDigests:
            if not CraftCore.settings.getboolean("Packager", "CreateCache"):
                self._generateManifest(destDir, archiveName)
                CraftHash.createDigestFiles(archive)
            else:
                if CraftCore.settings.getboolean("ContinuousIntegration", "UpdateRepository", False):
                    manifestUrls = [self.cacheRepositoryUrls()[0]]
                else:
                    manifestUrls = None
                self._generateManifest(destDir, archiveName, manifestLocation=self.cacheLocation(),
                                    manifestUrls=manifestUrls)
        return True

    def createPackage(self):
        """create 7z package with digest files located in the manifest subdir"""
        cacheMode = CraftCore.settings.getboolean("Packager", "CreateCache", False)
        if cacheMode:
            if self.subinfo.options.package.disableBinaryCache:
                return True
            dstpath = self.cacheLocation()
        else:
            dstpath = self.packageDestinationDir()


        extention = CraftCore.settings.get("Packager", "7ZipArchiveType",
                                           "7z" if OsUtils.isWin() else "tar.xz")

        self._compress(self.binaryArchiveName(fileType=extention, includePackagePath=cacheMode, includeTimeStamp=cacheMode), self.imageDir(), dstpath)
        if not self.subinfo.options.package.packSources:
            return True
        if CraftCore.settings.getboolean("Packager", "PackageSrc", "True"):
            self._compress(self.binaryArchiveName("-src", fileType=extention, includePackagePath=cacheMode, includeTimeStamp=cacheMode), self.sourceDir(), dstpath)
        return True
