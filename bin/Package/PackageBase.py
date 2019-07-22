#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from pathlib import Path

from CraftBase import *
from CraftCompiler import *
from InstallDB import *
from Blueprints.CraftPackageObject import *
from Utils import CraftHash, GetFiles, CraftChoicePrompt
from Utils.CraftManifest import CraftManifest

import json

class PackageBase(CraftBase):
    """
     provides a generic interface for packages and implements the basic stuff for all
     packages
    """

    # uses the following instance variables
    # todo: place in related ...Base

    # rootdir    -> CraftBase
    # package    -> PackageBase
    # force      -> PackageBase
    # category   -> PackageBase
    # version    -> PackageBase
    # packagedir -> PackageBase
    # imagedir   -> PackageBase

    def __init__(self):
        CraftCore.log.debug("PackageBase.__init__ called")
        CraftBase.__init__(self)

    def qmerge(self):
        """mergeing the imagedirectory into the filesystem"""
        ## \todo is this the optimal place for creating the post install scripts ?

        if self.package.isInstalled:
            self.unmerge()

        copiedFiles = []  # will be populated by the next call
        if not utils.copyDir(self.imageDir(), CraftCore.standardDirs.craftRoot(), copiedFiles=copiedFiles):
            return False

        # add package to installed database -> is this not the task of the manifest files ?

        revision = self.sourceRevision()
        package = CraftCore.installdb.addInstalled(self.package, self.version, revision=revision)
        fileList = self.getFileListFromDirectory(CraftCore.standardDirs.craftRoot(), copiedFiles)
        package.addFiles(fileList)
        package.install()

        if (CraftCore.settings.getboolean("Packager", "CreateCache") or
            CraftCore.settings.getboolean("Packager", "UseCache")):
            package.setCacheVersion(self.cacheVersion())

        return True

    def unmerge(self):
        """unmergeing the files from the filesystem"""
        CraftCore.log.debug("Packagebase unmerge called")
        packageList = CraftCore.installdb.getInstalledPackages(self.package)
        for package in packageList:
            fileList = package.getFilesWithHashes()
            self.unmergeFileList(CraftCore.standardDirs.craftRoot(), fileList)
            package.uninstall()
        return True

    def createImportLibs(self, pkgName):
        """create the import libraries for the other compiler(if ANSI-C libs)"""
        basepath = os.path.join(self.installDir())
        utils.createImportLibs(pkgName, basepath)

    def fetchBinary(self, downloadRetriesLeft=3) -> bool:
        if self.subinfo.options.package.disableBinaryCache:
            return False
        for url in [self.cacheLocation()] + self.cacheRepositoryUrls():
            CraftCore.log.debug(f"Trying to restore {self} from cache: {url}.")
            if url == self.cacheLocation():
                fileUrl = f"{url}/manifest.json"
                if os.path.exists(fileUrl):
                    with open(fileUrl, "rt", encoding="UTF-8") as f:
                        manifest = CraftManifest.fromJson(json.load(f))
                else:
                    continue
            else:
                manifest = CraftManifest.fromJson(CraftCore.cache.cacheJsonFromUrl(f"{url}/manifest.json"))
            fileEntry = manifest.get(str(self)).files
            files = []
            for f in fileEntry:
                if f.version == self.version:
                    files.append(f)
            if not files:
                CraftCore.log.debug(f"Could not find {self}={self.version} in {url}")
                continue
            latest = files[0]

            if latest.configHash and latest.configHash != self.subinfo.options.dynamic.configHash():
                CraftCore.log.warning("Failed to restore package, configuration missmatch")
                # try next cache
                continue

            # if we are creating the cache, a rebuild on a failed fetch would be suboptimal
            createingCache = CraftCore.settings.set("Packager", "CreateCache", False)

            if url != self.cacheLocation():
                downloadFolder = self.cacheLocation(os.path.join(CraftCore.standardDirs.downloadDir(), "cache"))
            else:
                downloadFolder = self.cacheLocation()
            localArchiveAbsPath = OsUtils.toNativePath(os.path.join(downloadFolder, latest.fileName))
            localArchivePath, localArchiveName = os.path.split(localArchiveAbsPath)


            if url != self.cacheLocation():
                if not os.path.exists(localArchiveAbsPath):
                    os.makedirs(localArchivePath, exist_ok=True)
                    fUrl = f"{url}/{latest.fileName}"
                    if not GetFiles.getFile(fUrl, localArchivePath, localArchiveName):
                        msg = f"Failed to fetch {fUrl}"
                        if createingCache:
                            raise BlueprintException(msg, self)
                        else:
                            CraftCore.log.warning(msg)
                        return False
            elif not os.path.isfile(localArchiveAbsPath):
                continue

            if not CraftHash.checkFilesDigests(localArchivePath, [localArchiveName],
                                               digests=latest.checksum,
                                               digestAlgorithm=CraftHash.HashAlgorithm.SHA256):
                msg = f"Hash did not match, {localArchiveName} might be corrupted"
                CraftCore.log.warning(msg)
                if downloadRetriesLeft and CraftChoicePrompt.promptForChoice("Do you want to delete the files and redownload them?",
                                                     [("Yes", True), ("No", False)],
                                                     default="Yes"):
                    return utils.deleteFile(localArchiveAbsPath) and self.fetchBinary(downloadRetriesLeft=downloadRetriesLeft-1)
                if createingCache:
                    raise BlueprintException(msg, self)
                return False
            self.subinfo.buildPrefix = latest.buildPrefix
            self.subinfo.isCachedBuild = True
            if not (self.cleanImage()
                    and utils.unpackFile(localArchivePath, localArchiveName, self.imageDir())
                    and self.internalPostInstall()
                    and self.postInstall()
                    and self.qmerge()
                    and self.internalPostQmerge()
                    and self.postQmerge()):
                return False
            return True
        return False

    @staticmethod
    def getFileListFromDirectory(imagedir, filePaths):
        """ create a file list containing hashes """
        ret = []

        algorithm = CraftHash.HashAlgorithm.SHA256
        for filePath in filePaths:
            relativeFilePath = os.path.relpath(filePath, imagedir)
            digest = algorithm.stringPrefix() + CraftHash.digestFile(filePath, algorithm)
            ret.append((relativeFilePath, digest))
        return ret

    @staticmethod
    def unmergeFileList(rootdir, fileList):
        """ delete files in the fileList if has matches """
        for filename, filehash in fileList:
            fullPath = os.path.join(rootdir, os.path.normcase(filename))
            if os.path.isfile(fullPath) or os.path.islink(fullPath):
                if filehash:
                    algorithm = CraftHash.HashAlgorithm.getAlgorithmFromPrefix(filehash)
                    currentHash = algorithm.stringPrefix() + CraftHash.digestFile(fullPath, algorithm)
                if not filehash or currentHash == filehash:
                    OsUtils.rm(fullPath, True)
                else:
                    CraftCore.log.warning(
                        f"We can't remove {fullPath} as its hash has changed,"
                        f" that usually implies that the file was modified or replaced")
            elif not os.path.isdir(fullPath) and os.path.lexists(fullPath):
                CraftCore.log.debug(f"Remove a dead symlink {fullPath}")
                OsUtils.rm(fullPath, True)
            elif not os.path.isdir(fullPath):
                CraftCore.log.warning("file %s does not exist" % fullPath)

            containingDir = os.path.dirname(fullPath)
            if os.path.exists(containingDir) and not os.listdir(containingDir):
                CraftCore.log.debug(f"Delete empty dir {containingDir}")
                utils.rmtree(containingDir)


    def runAction(self, command):
        functions = {"fetch": "fetch",
                     "cleanimage": "cleanImage",
                     "cleanbuild": "cleanBuild",
                     "unpack": "unpack",
                     "compile": "compile",
                     "configure": "configure",
                     "make": "make",
                     "install": ["install", "internalPostInstall"],
                     "post-install": "postInstall",
                     "test": "unittest",
                     "qmerge": ["qmerge", "internalPostQmerge"],
                     "post-qmerge": "postQmerge",
                     "unmerge": "unmerge",
                     "package": "createPackage",
                     "createpatch": "createPatch",
                     "checkdigest": "checkDigest",
                     "fetch-binary": "fetchBinary"}
        if command in functions:
            try:
                steps = functions[command]
                if not isinstance(steps, list):
                    steps = [steps]
                for step in steps:
                    if not getattr(self, step)():
                        return False
            except AttributeError as e:
                raise BlueprintException(str(e), self.package, e)

        else:
            CraftCore.log.error("command %s not understood" % command)
            return False
        return True
