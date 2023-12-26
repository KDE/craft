# -*- coding: utf-8 -*-
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
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

import datetime
import io
import os
import tempfile
from pathlib import Path

from CraftCore import CraftCore
from Source.SourceBase import *
from Utils import CraftChoicePrompt, CraftHash, GetFiles
from Utils.CraftManifest import CraftManifest


class ArchiveSource(SourceBase):
    """file download source"""

    def __init__(self):
        CraftCore.log.debug("ArchiveSource.__init__ called")
        SourceBase.__init__(self)
        self.__archiveDir = Path(CraftCore.standardDirs.downloadDir()) / "archives"
        self.__downloadDir = self.__archiveDir / self.package.path

    def __retry(self, downloadRetriesLeft: int, func, **kw):
        downloadRetriesLeft -= 1
        if downloadRetriesLeft >= 0 and CraftChoicePrompt.promptForChoice(
            "Do you want to delete the files and redownload them?",
            [("Yes", True), ("No", False)],
            default="Yes",
        ):
            return func(downloadRetriesLeft=downloadRetriesLeft, **kw)
        return False

    def localFileNames(self):
        if self.subinfo.archiveName() == [""]:
            urls = self.subinfo.targets[self.buildTarget]
            urls = urls if isinstance(urls, list) else [urls]
            return [os.path.basename(url) for url in urls]
        if isinstance(self.subinfo.archiveName(), (tuple, list)):
            return self.subinfo.archiveName()
        return [self.subinfo.archiveName()]

    def localFilePath(self):
        return [self.__downloadDir / f for f in self.localFileNames()]

    def __checkFilesPresent(self, filenames):
        def isFileValid(path):
            if not os.path.exists(path):
                return False

            return os.path.getsize(path) > 0

        """check if all files for the current target are available"""
        for filename in filenames:
            path = os.path.join(self.__downloadDir, filename)

            # check file
            if not isFileValid(path):
                return False

            # check digests
            if self.subinfo.hasTargetDigests():
                if not isFileValid(path):
                    return False
            elif self.subinfo.hasTargetDigestUrls():
                algorithm = CraftHash.HashAlgorithm.SHA1
                if type(self.subinfo.targetDigestUrl()) == tuple:
                    _, algorithm = self.subinfo.targetDigestUrl()
                if not isFileValid(path + algorithm.fileEnding()):
                    return False
        return True

    def fetch(self, downloadRetriesLeft=3):
        """fetch normal tarballs"""
        CraftCore.log.debug("ArchiveSource.fetch called")

        filenames = self.localFileNames()

        if self.noFetch:
            CraftCore.log.debug("skipping fetch (--offline)")
            return True

        if self.subinfo.hasTarget():
            if self.__checkFilesPresent(filenames):
                CraftCore.log.debug("files and digests available, no need to download files")
                return True
            if self.subinfo.target():
                # compat for scripts that provide multiple files
                files = (
                    zip(self.subinfo.target(), self.subinfo.archiveName())
                    if isinstance(self.subinfo.target(), list)
                    else [(self.subinfo.target(), self.subinfo.archiveName()[0])]
                )
                for url, fileName in files:
                    if not GetFiles.getFile(url, self.__downloadDir, fileName):
                        CraftCore.log.debug("failed to download files")
                        return False

                if self.subinfo.hasTargetDigestUrls():
                    if isinstance(self.subinfo.targetDigestUrl(), tuple):
                        url, alg = self.subinfo.targetDigestUrl()
                        return GetFiles.getFile(
                            url[0],
                            self.__downloadDir,
                            self.subinfo.archiveName()[0] + CraftHash.HashAlgorithm.fileEndings().get(alg),
                        )
                    else:
                        for url in self.subinfo.targetDigestUrl():
                            if not GetFiles.getFile(url, self.__downloadDir):
                                return False
                else:
                    CraftCore.log.debug("no digestUrls present")
            if downloadRetriesLeft and not self.__checkFilesPresent(filenames):
                return ArchiveSource.fetch(self, downloadRetriesLeft=downloadRetriesLeft - 1)
        return True

    def __redownload(self, downloadRetriesLeft: int, filenames):
        for filename in filenames:
            CraftCore.log.info(f"Deleting downloaded file: {filename}")
            utils.deleteFile(self.__downloadDir / filename)
            if self.subinfo.hasTargetDigestUrls():
                for (
                    digestAlgorithm,
                    digestFileEnding,
                ) in CraftHash.HashAlgorithm.fileEndings().items():
                    digestFileName = filename + digestFileEnding
                    if (self.__downloadDir / digestFileName).is_file():
                        CraftCore.log.info(f"Deleting downloaded file: {digestFileName}")
                        utils.deleteFile(self.__downloadDir / digestFileName)
        return self.fetch() and self.checkDigest(downloadRetriesLeft)

    def checkDigest(self, downloadRetriesLeft=3):
        CraftCore.log.debug("ArchiveSource.checkDigest called")
        filenames = self.localFileNames()
        if self.subinfo.hasTargetDigestUrls():
            CraftCore.log.debug("check digests urls")
            if not CraftHash.checkFilesDigests(self.__downloadDir, filenames):
                CraftCore.log.error("invalid digest file")
                return self.__retry(downloadRetriesLeft, self.__redownload, filenames=filenames)
        elif self.subinfo.hasTargetDigests():
            CraftCore.log.debug("check digests")
            digests, algorithm = self.subinfo.targetDigest()
            if not CraftHash.checkFilesDigests(self.__downloadDir, filenames, digests, algorithm):
                CraftCore.log.error("invalid digest file")
                return self.__retry(downloadRetriesLeft, self.__redownload, filenames=filenames)
        else:
            CraftCore.log.debug("print source file digests")
            CraftHash.printFilesDigests(
                self.__downloadDir,
                filenames,
                self.subinfo.buildTarget,
                algorithm=CraftHash.HashAlgorithm.SHA256,
            )
        return True

    def unpack(self):
        """unpacking all zipped(gz, zip, bz2) tarballs"""
        CraftCore.log.debug("ArchiveSource.unpack called")

        filenames = self.localFileNames()

        # TODO: this might delete generated patches
        utils.cleanDirectory(self.workDir())

        if not self.checkDigest(3):
            return False

        for filename in filenames:
            if not filename:
                continue
            ext = Path(filename).suffix
            if not ext or ext in {".exe", ".bat", ".msi", ".AppImage"}:
                filePath = os.path.abspath(os.path.join(self.__downloadDir, filename))
                if self.subinfo.options.unpack.runInstaller:
                    if ext == ".exe":
                        return utils.system("%s %s" % (filePath, self.subinfo.options.configure.args))
                    elif ext == ".msi":
                        return utils.system("msiexec /package %s %s" % (filePath, self.subinfo.options.configure.args))
                if not utils.copyFile(filePath, os.path.join(self.workDir(), filename)):
                    return False
            else:
                if not utils.unpackFile(self.__downloadDir, filename, self.workDir()):
                    return False

        return self.applyPatches()

    def getUrls(self):
        CraftCore.debug.printOut(self.subinfo.target())
        CraftCore.debug.printOut(self.subinfo.targetDigestUrl())
        return True

    def createPatch(self):
        """unpacking all zipped(gz, zip, bz2) tarballs a second time and making a patch"""

        if not CraftCore.cache.findApplication("diff"):
            CraftCore.log.critical("could not find diff tool, please run 'craft diffutils'")
            return False

        # get the file paths of the tarballs
        filenames = self.localFileNames()

        destdir = self.workDir()

        # it makes no sense to make a diff against nothing
        if not os.path.exists(self.sourceDir()):
            CraftCore.log.error("source directory doesn't exist, please run unpack first")
            return False

        CraftCore.log.debug("unpacking files into work root %s" % destdir)

        # make a temporary directory so the original packages don't overwrite the already existing ones
        with tempfile.TemporaryDirectory() as tmpdir:
            _patchName = f"{self.package.name}-{self.buildTarget}-{str(datetime.date.today()).replace('-', '')}.diff"

            # unpack all packages
            for filename in filenames:
                CraftCore.log.debug(f"unpacking this file: {filename}")
                if not utils.unpackFile(self.__downloadDir, filename, tmpdir):
                    return False

            patches = self.subinfo.patchesToApply()
            if not isinstance(patches, list):
                patches = [patches]
            for fileName, patchdepth in patches:
                if os.path.basename(fileName) == _patchName:
                    CraftCore.log.info(f"skipping patch {fileName} with patchlevel: {patchdepth}")
                    continue
                CraftCore.log.info(f"applying patch {fileName} with patchlevel: {patchdepth}")
                if not self.applyPatch(
                    fileName,
                    patchdepth,
                    os.path.join(tmpdir, os.path.relpath(self.sourceDir(), self.workDir())),
                ):
                    return False

            srcSubDir = os.path.relpath(self.sourceDir(), self.workDir())
            tmpSourceDir = os.path.join(tmpdir, srcSubDir)
            with io.BytesIO() as out:
                ignores = []
                for x in [
                    "*~",
                    r"*\.rej",
                    r"*\.orig",
                    r"*\.o",
                    r"*\.pyc",
                    "CMakeLists.txt.user",
                ]:
                    ignores += ["-x", x]

                # TODO: actually we should not accept code 2
                if not utils.system(
                    ["diff", "-Nrub"] + ignores + [tmpSourceDir, self.sourceDir()],
                    stdout=out,
                    acceptableExitCodes=[0, 1, 2],
                    cwd=destdir,
                ):
                    return False
                patchContent = out.getvalue()
            # make the patch a -p1 patch
            patchContent = patchContent.replace(tmpSourceDir.encode(), f"{srcSubDir}.orig".encode())
            patchContent = patchContent.replace(str(self.sourceDir()).encode(), srcSubDir.encode())
            patchPath = os.path.join(self.packageDir(), _patchName)
            with open(patchPath, "wb") as out:
                out.write(patchContent)

            CraftCore.log.info(f'Patch created {patchPath} self.patchToApply["{self.buildTarget}"] = [("{_patchName}", 1)]')
        return True

    def sourceVersion(self):
        """return a version based on the file name of the current target"""
        # we hope that the build target is equal to the version that is build
        return self.subinfo.buildTarget
