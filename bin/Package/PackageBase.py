#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from CraftBase import *
from CraftCompiler import *
from InstallDB import *
from Blueprints.CraftPackageObject import *
from Utils import CraftHash
from Utils.CraftManifest import CraftManifest


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
        utils.copyDir(self.imageDir(), CraftCore.standardDirs.craftRoot(), copiedFiles=copiedFiles)

        # run post-install scripts
        if not CraftCore.settings.getboolean("General", "EMERGE_NO_POST_INSTALL", False):
            for pkgtype in ['bin', 'lib', 'doc', 'src']:
                scriptName = "post-install-%s-%s.cmd" % (self.package, pkgtype)
                script = os.path.join(CraftCore.standardDirs.craftRoot(), "manifest", scriptName)
                if os.path.exists(script):
                    CraftCore.log.debug("run post install script '%s'" % script)
                    cmd = "cd /D %s && %s" % (CraftCore.standardDirs.craftRoot(), script)
                    if not utils.system(cmd):
                        CraftCore.log.warning("%s failed!" % cmd)
                else:
                    CraftCore.log.debug("post install script '%s' not found" % script)
        else:
            CraftCore.log.debug("running of post install scripts disabled!")

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

        # run post-uninstall scripts
        if not CraftCore.settings.getboolean("General", "EMERGE_NO_POST_INSTALL", False):
            for pkgtype in ['bin', 'lib', 'doc', 'src']:
                scriptName = "post-uninstall-%s-%s.cmd" % (self.package, pkgtype)
                script = os.path.join(CraftCore.standardDirs.craftRoot(), "manifest", scriptName)
                if os.path.exists(script):
                    CraftCore.log.debug("run post uninstall script '%s'" % script)
                    cmd = "cd /D %s && %s" % (CraftCore.standardDirs.craftRoot(), script)
                    if not utils.system(cmd):
                        CraftCore.log.warning("%s failed!" % cmd)
                else:
                    CraftCore.log.debug("post uninstall script '%s' not found" % script)
        else:
            CraftCore.log.debug("running of post uninstall scripts disabled!")

        return True

    def cleanImage(self) -> bool:
        """cleanup before install to imagedir"""
        if (os.path.exists(self.imageDir())):
            CraftCore.log.debug("cleaning image dir: %s" % self.imageDir())
            utils.cleanDirectory(self.imageDir())
            os.rmdir(self.imageDir())
        return True

    def cleanBuild(self) -> bool:
        """cleanup currently used build dir"""
        if os.path.exists(self.buildDir()):
            utils.cleanDirectory(self.buildDir())
            CraftCore.log.debug("cleaning build dir: %s" % self.buildDir())

        return True

    def strip(self, fileName):
        """strip debugging informations from shared libraries and executables - mingw only!!! """
        if self.subinfo.options.package.disableStriping or not CraftCore.compiler.isGCCLike():
            CraftCore.log.debug(f"Skipping stripping of {fileName} -- either disabled or unsupported with this compiler")
            return True

        if OsUtils.isMac():
            CraftCore.log.debug(f"Skipping stripping of files on macOS -- not implemented")
            return True

        if os.path.isabs(fileName):
            filepath = fileName
        else:
            CraftCore.log.warning("Please pass an absolute file path to strip")
            basepath = os.path.join(self.installDir())
            filepath = os.path.join(basepath, "bin", fileName)
        return utils.system(["strip", "-s", filepath])

    def createImportLibs(self, pkgName):
        """create the import libraries for the other compiler(if ANSI-C libs)"""
        basepath = os.path.join(self.installDir())
        utils.createImportLibs(pkgName, basepath)

    def printFiles(self):
        packageList = CraftCore.installdb.getInstalledPackages(self.package)
        for package in packageList:
            fileList = package.getFiles()
            fileList.sort()
            for file in fileList:
                print(file[0])
        return True

    def getAction(self, cmd=None):
        if not cmd:
            command = sys.argv[1]
            options = None
            #            print sys.argv
            if (len(sys.argv) > 2):
                options = sys.argv[2:]
        else:
            command = cmd
            options = None
        # \todo options are not passed through by craft.py fix it
        return [command, options]

    def execute(self, cmd=None):
        """called to run the derived class
        this will be executed from the package if the package is started on its own
        it shouldn't be called if the package is imported as a python module"""

        CraftCore.log.debug("PackageBase.execute called. args: %s" % sys.argv)
        command, _ = self.getAction(cmd)

        return self.runAction(command)

    def fetchBinary(self) -> bool:
        if self.subinfo.options.package.disableBinaryCache:
            return False

        for url in [self.cacheLocation()] + self.cacheRepositoryUrls():
            CraftCore.log.debug(f"Trying to restore {self} from cache: {url}.")
            manifest = CraftManifest.fromJson(CraftCore.cache.cacheJsonFromUrl(f"{url}/manifest.json"))
            fileEntry = manifest.get(str(self)).files
            files = []
            for f in fileEntry:
                if f.version == self.version:
                    files.append(f)
            latest = None
            if files:
                latest = files[0]
            elif fileEntry:
                # legacy remove at some point
                latest = fileEntry[0] if fileEntry else None
                if not latest or self.version not in latest.fileName and "-latest-" not in latest.fileName:
                    continue
            if not latest:
                continue

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
                    if not utils.getFile(fUrl, localArchivePath, localArchiveName):
                        CraftCore.log.warning(f"Failed to fetch {fUrl}")
                        return False
            if not CraftHash.checkFilesDigests(localArchivePath, [localArchiveName],
                                               digests=latest.checksum,
                                               digestAlgorithm=CraftHash.HashAlgorithm.SHA256):
                CraftCore.log.warning(f"Hash did not match, {localArchiveName} might be corrupted")
                return False
            if not (self.cleanImage()
                    and utils.unpackFile(localArchivePath, localArchiveName, self.imageDir())
                    and self.qmerge()):
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
            if OsUtils.isUnix() and os.path.islink(filePath):
                digest = ""
            else:
                digest = algorithm.stringPrefix() + CraftHash.digestFile(filePath, algorithm)
            ret.append((relativeFilePath, digest))
        return ret

    @staticmethod
    def unmergeFileList(rootdir, fileList):
        """ delete files in the fileList if has matches """
        for filename, filehash in fileList:
            fullPath = os.path.join(rootdir, os.path.normcase(filename))
            if os.path.isfile(fullPath):
                algorithm = CraftHash.HashAlgorithm.getAlgorithmFromPrefix(filehash)
                if not algorithm:
                    currentHash = CraftHash.digestFile(fullPath, CraftHash.HashAlgorithm.MD5)
                else:
                    currentHash = algorithm.stringPrefix() + CraftHash.digestFile(fullPath, algorithm)
                if currentHash == filehash or filehash == "":
                    OsUtils.rm(fullPath, True)
                else:
                    CraftCore.log.warning(
                        f"We can't remove {fullPath} as its hash has changed,"
                        f" that usually implies that the fiel was modified or replaced")
            elif not os.path.isdir(fullPath):
                CraftCore.log.warning("file %s does not exist" % fullPath)

    def runAction(self, command):
        """ \todo TODO: rename the internal functions into the form cmdFetch, cmdCheckDigest etc
        then we get by without this dict:
            ok = getattr(self, 'cmd' + command.capitalize()()
        next we could """
        functions = {"fetch": "fetch",
                     "cleanimage": "cleanImage",
                     "cleanbuild": "cleanBuild",
                     "unpack": "unpack",
                     "compile": "compile",
                     "configure": "configure",
                     "make": "make",
                     "install": "install",
                     "test": "unittest",
                     "qmerge": "qmerge",
                     "unmerge": "unmerge",
                     "package": "createPackage",
                     "createpatch": "createPatch",
                     "print-files": "printFiles",
                     "checkdigest": "checkDigest",
                     "fetch-binary": "fetchBinary"}
        if command in functions:
            try:
                ok = getattr(self, functions[command])()
            except AttributeError as e:
                raise BlueprintException(str(e), self.package, e)

        else:
            ok = CraftCore.log.error("command %s not understood" % command)

        return ok
