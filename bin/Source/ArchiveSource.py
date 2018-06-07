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

import tempfile
import io

from Source.SourceBase import *
from Utils import CraftHash

from CraftCore import CraftCore


class ArchiveSource(SourceBase):
    """ file download source"""

    def __init__(self):
        CraftCore.log.debug("ArchiveSource.__init__ called")
        SourceBase.__init__(self)
        self.__downloadDir = os.path.abspath(os.path.join(CraftCore.standardDirs.downloadDir(), "archives", self.package.path))

    def localFileNames(self):
        if self.subinfo.archiveName() == [""]:
            return self.localFileNamesBase()
        if isinstance(self.subinfo.archiveName(), (tuple, list)):
            return self.subinfo.archiveName()
        return [self.subinfo.archiveName()]

    def localFileNamesBase(self):
        """ collect local filenames """
        CraftCore.log.debug("ArchiveSource.localFileNamesBase called")

        filenames = []
        for url in self.subinfo.targets.values():
            filenames.append(os.path.basename(url))
        return filenames

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

    def fetch(self):
        """fetch normal tarballs"""
        CraftCore.log.debug("ArchiveSource.fetch called")

        filenames = self.localFileNames()

        if (self.noFetch):
            CraftCore.log.debug("skipping fetch (--offline)")
            return True

        if self.subinfo.hasTarget():
            if self.__checkFilesPresent(filenames):
                CraftCore.log.debug("files and digests available, no need to download files")
                return True

            result = utils.getFiles(self.subinfo.target(), self.__downloadDir,
                                    filenames=self.subinfo.archiveName())
            if not result:
                CraftCore.log.debug("failed to download files")
                return False
            if result and self.subinfo.hasTargetDigestUrls():
                if type(self.subinfo.targetDigestUrl()) == tuple:
                    url, alg = self.subinfo.targetDigestUrl()
                    return utils.getFiles(url, self.__downloadDir,
                                          filenames=self.subinfo.archiveName()[0]
                                                    + CraftHash.HashAlgorithm.fileEndings().get(alg))
                else:
                    return utils.getFiles(self.subinfo.targetDigestUrl(), self.__downloadDir, filenames='')
            else:
                CraftCore.log.debug("no digestUrls present")
                return True
        else:
            return utils.getFiles("", self.__downloadDir)

    def checkDigest(self):
        CraftCore.log.debug("ArchiveSource.checkDigest called")
        filenames = self.localFileNames()

        if self.subinfo.hasTargetDigestUrls():
            CraftCore.log.debug("check digests urls")
            if not CraftHash.checkFilesDigests(self.__downloadDir, filenames):
                CraftCore.log.error("invalid digest file")
                return False
        elif self.subinfo.hasTargetDigests():
            CraftCore.log.debug("check digests")
            digests, algorithm = self.subinfo.targetDigest()
            if not CraftHash.checkFilesDigests(self.__downloadDir, filenames, digests, algorithm):
                CraftCore.log.error("invalid digest file")
                return False
        else:
            CraftCore.log.debug("print source file digests")
            CraftHash.printFilesDigests(self.__downloadDir, filenames, self.subinfo.buildTarget,
                                        algorithm=CraftHash.HashAlgorithm.SHA256)
        return True

    def unpack(self):
        """unpacking all zipped(gz, zip, bz2) tarballs"""
        CraftCore.log.debug("ArchiveSource.unpack called")

        filenames = self.localFileNames()

        # TODO: this might delete generated patches
        utils.cleanDirectory(self.workDir())

        if not self.checkDigest():
            return False

        binEndings = (".exe", ".bat", ".msi")
        for filename in filenames:
            if filename.endswith(binEndings):
                filePath = os.path.abspath(os.path.join(self.__downloadDir, filename))
                if self.subinfo.options.unpack.runInstaller:
                    _, ext = os.path.splitext(filename)
                    if ext == ".exe":
                        return utils.system("%s %s" % (filePath, self.subinfo.options.configure.args))
                    elif (ext == ".msi"):
                        return utils.system("msiexec /package %s %s" % (filePath, self.subinfo.options.configure.args))
                if not utils.copyFile(filePath, os.path.join(self.workDir(), filename)):
                    return False
            else:
                if not utils.unpackFile(self.__downloadDir, filename, self.workDir()):
                    return False

        ret = self.applyPatches()
        if CraftCore.settings.getboolean("General", "EMERGE_HOLD_ON_PATCH_FAIL", False):
            return ret
        return True

    def getUrls(self):
        print(self.subinfo.target())
        print(self.subinfo.targetDigestUrl())
        return True

    def createPatch(self):
        """ unpacking all zipped(gz, zip, bz2) tarballs a second time and making a patch """

        if not os.path.exists(CraftCore.cache.findApplication("diff")):
            CraftCore.log.critical("could not find diff tool, please run 'craft diffutils'")

        # get the file paths of the tarballs
        filenames = self.localFileNames()

        destdir = self.workDir()

        # it makes no sense to make a diff against nothing
        if (not os.path.exists(self.sourceDir())):
            CraftCore.log.error("source directory doesn't exist, please run unpack first")
            return False

        CraftCore.log.debug("unpacking files into work root %s" % destdir)

        # make a temporary directory so the original packages don't overwrite the already existing ones
        with tempfile.TemporaryDirectory() as tmpdir:
            # unpack all packages
            for filename in filenames:
                CraftCore.log.debug("unpacking this file: %s" % filename)
                if (not utils.unpackFile(self.__downloadDir, filename, tmpdir)):
                    return False

            patches = self.subinfo.patchesToApply()
            if not isinstance(patches, list):
                patches = [patches]
            for fileName, patchdepth in patches:
                CraftCore.log.debug("applying patch %s with patchlevel: %s" % (fileName, patchdepth))
                if not self.applyPatch(fileName, patchdepth, os.path.join(tmpdir, os.path.relpath(self.sourceDir(), self.workDir()))):
                    return False

            date = str(datetime.date.today()).replace("-", "")
            _patchName = os.path.join(self.packageDir(), f"{self.package.name}-{self.buildTarget}-{date}.diff")

            with io.BytesIO() as out:
                # TODO: actually we should not accept code 2
                if not utils.system(["diff", "-Nrub",
                                        "-x", "*~", "-x", "*\\.rej", "-x", "*\\.orig", "-x", "*\\.o", "-x", "*\\.pyc",
                                        "-x", f"{os.path.basename(self.buildDir())}*",#ignore the build dir
                                        tmpdir, self.workDir()],
                                    stdout=out, acceptableExitCodes=[0,1,2], cwd=destdir):
                    return False
                patchContent = out.getvalue()
            # make the patch a -p2 patch
            patchContent = patchContent.replace(tmpdir.encode(), b"a")
            patchContent = patchContent.replace(self.workDir().encode(), b"b")
            with open(_patchName, "wb") as out:
                out.write(patchContent)

            CraftCore.log.info(f"Patch created ('{_patchName}', 2)")
        return True

    def sourceVersion(self):
        """ return a version based on the file name of the current target """
        # we hope that the build target is equal to the version that is build
        return self.subinfo.buildTarget
