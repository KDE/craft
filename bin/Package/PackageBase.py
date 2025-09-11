#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import dataclasses
import json
import os
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import BlueprintException
from CraftBase import CraftBase
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Utils import CraftChoicePrompt, CraftHash, GetFiles
from Utils.CraftManifest import CraftManifest, FileType


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

    def __init__(self, **kwargs):
        CraftCore.log.debug("PackageBase.__init__ called")
        CraftBase.__init__(self, **kwargs)

    def qmerge(self, dbOnly=False):
        """mergeing the imagedirectory into the filesystem"""
        CraftCore.log.debug("PackageBase.qmerge called")
        # \todo is this the optimal place for creating the post install scripts ?

        if self.package.isInstalled:
            self.unmerge(dbOnly=dbOnly)

        copiedFiles = []  # will be populated by the next call
        if not dbOnly:
            for imageDir in [self.imageDir(), self.symbolsImageDir()]:
                if imageDir.exists():
                    if not utils.copyDir(
                        imageDir,
                        CraftCore.standardDirs.craftRoot(),
                        copiedFiles=copiedFiles,
                    ):
                        return False

        # add package to installed database -> is this not the task of the manifest files ?

        revision = self.sourceRevision()
        package = CraftCore.installdb.addInstalled(self.package, self.version, revision=revision)
        if not dbOnly:
            fileList = self.getFileListFromDirectory(CraftCore.standardDirs.craftRoot(), copiedFiles)
            package.addFiles(fileList)
        package.install()

        if CraftCore.settings.getboolean("Packager", "CreateCache") or CraftCore.settings.getboolean("Packager", "UseCache"):
            package.setCacheVersion(self.cacheVersion())

        return True

    def unmerge(self, dbOnly=False):
        """unmergeing the files from the filesystem"""
        CraftCore.log.debug("PackageBase.unmerge called")
        packageList = CraftCore.installdb.getInstalledPackages(self.package)
        for package in packageList:
            if not dbOnly:
                fileList = package.getFilesWithHashes()
                self.unmergeFileList(CraftCore.standardDirs.craftRoot(), fileList)
            package.uninstall()
        return True

    def fetchBinary(self, downloadRetriesLeft=3) -> bool:
        if self.subinfo.options.package.disableBinaryCache:
            return False
        for url in [self.cacheLocation()] + self.cacheRepositoryUrls():
            CraftCore.log.debug(f"Trying to restore {self} from cache: {url}")
            if url == self.cacheLocation():
                fileUrl = f"{url}/manifest.json"
                if os.path.exists(fileUrl):
                    with open(fileUrl, "rt", encoding="UTF-8") as f:
                        manifest = CraftManifest.fromJson(json.load(f))
                else:
                    continue
            else:
                manifest = CraftManifest.fromJson(CraftCore.cache.cacheJsonFromUrl(f"{url}/manifest.json"))
            fileEntry = manifest.get(str(self)).build
            allFiles = []
            for f in fileEntry:
                if f.version == self.version:
                    allFiles.append(f)
            if not allFiles:
                CraftCore.log.info(f"Could not find {self}={self.version} in {url}")
                continue
            latest = allFiles[0]

            if not self.subinfo.options.dynamic.compatible(latest.config, latest.configHash):
                CraftCore.log.info("Failed to restore package, configuration missmatch")
                CraftCore.debug.debug_line()
                CraftCore.log.info(f'Cached config: {", ".join(f"{k}={v}" for k, v in latest.config.items())}')
                CraftCore.log.info(f"Local config:  {self.subinfo.options.dynamic}")
                CraftCore.debug.debug_line()
                # try next cache
                continue

            # if we are creating the cache, a rebuild on a failed fetch would be suboptimal
            createingCache = CraftCore.settings.getboolean("Packager", "CreateCache", False)

            if url != self.cacheLocation():
                downloadFolder = self.cacheLocation(os.path.join(CraftCore.standardDirs.downloadDir(), "cache"))
            else:
                downloadFolder = self.cacheLocation()

            files: dict[FileType, tuple[str, str]] = {}
            fileTypes = [FileType.Binary]
            if CraftCore.settings.getboolean("Packager", "DownloadDebugSymbolsCache", False):
                fileTypes += [FileType.Debug]
            for type in fileTypes:
                if type not in latest.files:
                    continue
                fileObject = latest.files[type]
                localArchiveAbsPath = downloadFolder / fileObject.fileName

                if url != self.cacheLocation():
                    if not localArchiveAbsPath.exists():
                        if not utils.createDir(localArchiveAbsPath.parent):
                            return False
                        fileName = fileObject.fileName
                        if CraftCore.compiler.platform.isWindows:
                            fileName = fileName.replace("\\", "/")
                        fUrl = f"{url}/{fileName}"
                        # try it up to 3 times
                        retries = 3
                        while True:
                            if GetFiles.getFile(
                                fUrl,
                                localArchiveAbsPath.parent,
                                localArchiveAbsPath.name,
                            ):
                                break
                            msg = f"Failed to fetch {fUrl}"
                            retries -= 1
                            if not retries:
                                if createingCache:
                                    raise BlueprintException(msg, self.package)
                                else:
                                    CraftCore.log.warning(msg)
                                return False
                elif not localArchiveAbsPath.is_file():
                    continue
                # file exist locally was downloaded or already existed
                files[type] = localArchiveAbsPath
                if not CraftHash.checkFilesDigests(
                    localArchiveAbsPath.parent,
                    [localArchiveAbsPath.name],
                    digests=fileObject.checksum,
                    digestAlgorithm=CraftHash.HashAlgorithm.SHA256,
                ):
                    msg = f"Hash did not match, {localArchiveAbsPath} might be corrupted"
                    CraftCore.log.warning(msg)
                    if downloadRetriesLeft and CraftChoicePrompt.promptForChoice(
                        "Do you want to delete the files and redownload them?",
                        [("Yes", True), ("No", False)],
                        default="Yes",
                    ):
                        return utils.deleteFile(localArchiveAbsPath) and self.fetchBinary(downloadRetriesLeft=downloadRetriesLeft - 1)
                    if createingCache:
                        raise BlueprintException(msg, self.package)
                    return False
            if not files:
                # try the next url
                continue
            self.subinfo.buildPrefix = latest.buildPrefix
            self.subinfo.revision = latest.revision
            self.subinfo.isCachedBuild = True
            if not self.cleanImage():
                return False

            dest = {
                FileType.Binary: self.imageDir(),
                FileType.Debug: self.symbolsImageDir(),
            }
            for type, localArchivePath in files.items():
                if not utils.cleanDirectory(dest[type]) or not utils.unpackFile(localArchivePath.parent, localArchivePath.name, dest[type]):
                    return False
            if not (self.internalPostInstall() and self.postInstall() and self.qmerge() and self.internalPostQmerge() and self.postQmerge()):
                return False
            return True
        return False

    @staticmethod
    def getFileListFromDirectory(imagedir, filePaths):
        """create a file list containing hashes"""
        ret = []

        algorithm = CraftHash.HashAlgorithm.SHA256
        for filePath in filePaths:
            relativeFilePath = os.path.relpath(filePath, imagedir)
            digest = algorithm.stringPrefix() + CraftHash.digestFile(filePath, algorithm)
            ret.append((relativeFilePath, digest))
        return ret

    @staticmethod
    def unmergeFileList(rootdir, fileList):
        """delete files in the fileList if has matches"""
        rootdir = Path(rootdir)

        @dataclasses.dataclass
        class File:
            path: Path
            hash: str

        fileList = [File(rootdir / file, hash) for file, hash in fileList]
        # ensure the files are sorted, that way we can delete empty dirs when going a lvl up
        fileList = sorted(fileList, key=lambda x: (len(x.path.parents), x.path))

        while len(fileList) > 0:
            file = fileList.pop()
            if file.path.is_file():
                if file.hash:
                    algorithm = CraftHash.HashAlgorithm.getAlgorithmFromPrefix(file.hash)
                    currentHash = algorithm.stringPrefix() + CraftHash.digestFile(file.path, algorithm)
                if not file.hash or currentHash == file.hash:
                    OsUtils.rm(file.path, True)
                else:
                    CraftCore.log.warning(
                        f"We can't remove {file.path} as its hash has changed," f" that usually implies that the file was modified or replaced"
                    )
            elif file.path.is_symlink():
                if file.path.is_dir():
                    CraftCore.log.debug(f"Remove symlink {file.path} to a directory")
                else:
                    CraftCore.log.debug(f"Remove a dead symlink {file.path}")
                OsUtils.rm(file.path, True)
            elif not file.path.is_dir():
                CraftCore.log.warning(f"file {file.path} does not exist")

            # if we are the last element in the list or the next parent is a different path
            # check whether we are in an empty dir that we should remove
            if not fileList or fileList[-1].path.parent != file.path.parent:
                containingDir = file.path.parent
                if containingDir.exists() and not any(containingDir.iterdir()):
                    CraftCore.log.debug(f"Delete empty dir {containingDir}")
                    utils.rmtree(containingDir)

    def _update(self):
        from Source.GitSource import GitSource

        if not self.fetch():
            return False
        if isinstance(self, GitSource):
            revision = self.sourceRevision()
            installed = CraftCore.installdb.getInstalledPackages(self.package)[0]
            if revision == installed.getRevision():
                return True
        # TODO: handle the internal steps more sane
        return self.configure() and self.make() and self.install() and self.internalPostInstall() and self.postInstall() and self.qmerge() and self.postQmerge()

    def runAction(self, command):
        # TODO: handle the internal steps more sane
        functions = {
            "fetch": "fetch",
            "cleanimage": "cleanImage",
            "cleanbuild": "cleanBuild",
            "unpack": "unpack",
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
            "fetch-binary": "fetchBinary",
            "update": "_update",
        }
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
            CraftCore.log.error(f"command {command} not understood")
            return False
        return True
