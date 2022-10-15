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

from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.PackageBase import InitGuard
from Packager.PackagerBase import PackagerBase
from Utils import CraftHash
from Utils.CraftManifest import CraftManifest, FileType


class SevenZipPackager(PackagerBase):
    """Packager using the 7za command line tool from the dev-utils/7zip package"""

    @InitGuard.init_once
    def __init__(self):
        PackagerBase.__init__(self)

    def createPackage(self):
        """create 7z package with digest files located in the manifest subdir"""
        cacheMode = CraftCore.settings.getboolean("Packager", "CreateCache", False)
        if cacheMode:
            if self.subinfo.options.package.disableBinaryCache:
                return True
            dstpath = self.cacheLocation()
        else:
            dstpath = self.packageDestinationDir()

        files = [
            (
                FileType.Binary,
                self.binaryArchiveName(
                    fileType=self.archiveExtension,
                    includePackagePath=cacheMode,
                    includeTimeStamp=cacheMode,
                ),
                self.imageDir(),
            )
        ]

        if (
            CraftCore.settings.getboolean("Packager", "PackageDebugSymbols", False)
            and self.symbolsImageDir().exists()
        ):
            files += [
                (
                    FileType.Debug,
                    self.binaryArchiveName(
                        "-dbg",
                        fileType=self.archiveExtension,
                        includePackagePath=cacheMode,
                        includeTimeStamp=cacheMode,
                    ),
                    self.symbolsImageDir(),
                )
            ]

        if (
            self.subinfo.options.package.packSources
            and CraftCore.settings.getboolean("Packager", "PackageSrc", "True")
            and self.sourceDir().exists()
        ):
            files += [
                (
                    FileType.Source,
                    self.binaryArchiveName(
                        "-src",
                        fileType=self.archiveExtension,
                        includePackagePath=cacheMode,
                        includeTimeStamp=cacheMode,
                    ),
                    self.sourceDir(),
                )
            ]

        for _, archive, sourceDir in files:
            if not self._createArchive(
                archive, sourceDir, dstpath, createDigests=not cacheMode
            ):
                return False

        if cacheMode:
            if CraftCore.settings.getboolean(
                "ContinuousIntegration", "UpdateRepository", False
            ):
                manifestUrls = [self.cacheRepositoryUrls()[0]]
            else:
                CraftCore.log.warning(
                    f'Creating new cache, if you want to extend an existing cache, set "[ContinuousIntegration]UpdateRepository = True"'
                )
                manifestUrls = None

            manifestLocation = dstpath / "manifest.json"
            manifest = CraftManifest.load(manifestLocation, urls=manifestUrls)
            entry = manifest.get(str(self))
            package = entry.addBuild(self.version, self.subinfo.options.dynamic)
            for type, archiveName, _ in files:
                package.addFile(
                    type,
                    archiveName,
                    CraftHash.digestFile(
                        dstpath / archiveName, CraftHash.HashAlgorithm.SHA256
                    ),
                )
            manifest.dump(manifestLocation)
        return True
