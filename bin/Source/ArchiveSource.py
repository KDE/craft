#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

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

        diffExe = os.path.join(self.rootdir, "dev-utils", "bin", "diff.exe")
        if not os.path.exists(diffExe):
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
        tmpdir = os.path.join(destdir, "tmp")
        unpackDir = tmpdir

        utils.cleanDirectory(unpackDir)

        if (not os.path.exists(unpackDir)):
            os.mkdir(unpackDir)

            if (not os.path.exists(unpackDir)):
                os.mkdir(unpackDir)

        # unpack all packages
        for filename in filenames:
            CraftCore.log.debug("unpacking this file: %s" % filename)
            if (not utils.unpackFile(self.__downloadDir, filename, unpackDir)):
                return False

        packagelist = os.listdir(tmpdir)

        # apply all patches only ommitting the last one, this makes it possible to always work on the latest patch
        # for future work, it might be interesting to switch patches on and off at will, this probably needs an
        # own patch management though
        patchName = None
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            patches = self.subinfo.patchesToApply()
            if not isinstance(patches, list):
                patches = [patches]
            for fileName, patchdepth in patches[:-1]:
                CraftCore.log.debug("applying patch %s with patchlevel: %s" % (fileName, patchdepth))
                if not self.applyPatch(fileName, patchdepth, os.path.join(tmpdir, packagelist[0])):
                    return False
            # we cant use the same name if we have more than one file to diff
            if len(packagelist) == 1 and patches[-1][0]:
                patchName = os.path.join(self.buildRoot(), patches[-1][0])

        # move the packages up and rename them to be different from the original source directory
        for directory in packagelist:
            # if the source or dest directory already exists, remove the occurance instead
            dest = os.path.join(destdir, f"{directory}.orig")
            if os.path.isdir(dest):
                utils.rmtree(dest)
                utils.moveDir(os.path.join(tmpdir, directory), dest)
            else:
                utils.deleteFile(dest)
                utils.moveFile(os.path.join(tmpdir, directory), dest)

        os.chdir(destdir)

        for directory in packagelist:
            if not patchName:
                date = str(datetime.date.today()).replace("-", "")
                _patchName = os.path.join(self.buildRoot(), f"{directory}-{date}.diff")
            else:
                _patchName = patchName

            with open(_patchName, "wb") as out:
                CraftCore.log.info(f"Creating patch {_patchName}")
                # TODO: actually we should not accept code 2
                if not utils.system(["diff", "-Nrub",
                                     "-x", "*~", "-x", "*\\.rej", "-x", "*\\.orig", "-x*\\.o", "-x", "*\\.pyc",
                                     f"{directory}.orig", directory],
                                    stdout=out, acceptableExitCodes=[0,1,2]):
                    return False

        CraftCore.log.debug("patch created at %s" % patchName)
        # remove all directories that are not needed any more after making the patch
        # disabled for now
        # for directory in packagelist:
        #    shutil.rmtree( directory + ".orig" )

        # remove the temporary directory, it should be empty after all directories have been moved up
        os.rmdir(tmpdir)

        return True

    def sourceVersion(self):
        """ return a version based on the file name of the current target """
        # we hope that the build target is equal to the version that is build
        return self.subinfo.buildTarget
