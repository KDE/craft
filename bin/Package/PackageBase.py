#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import CraftHash
from CraftBase import *
from CraftCompiler import *
from InstallDB import *
from Portage.CraftPackageObject import *


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
        craftDebug.log.debug("PackageBase.__init__ called")
        CraftBase.__init__(self)

    def qmerge(self):
        """mergeing the imagedirectory into the filesystem"""
        ## \todo is this the optimal place for creating the post install scripts ?

        if installdb.isInstalled(package=self.package):
            self.unmerge()

        craftDebug.log.debug("qmerge package to %s" % self.mergeDestinationDir())

        copiedFiles = []  # will be populated by the next call
        utils.copyDir(self.mergeSourceDir(), self.mergeDestinationDir(), copiedFiles=copiedFiles)

        # run post-install scripts
        if not craftSettings.getboolean("General", "EMERGE_NO_POST_INSTALL", False):
            for pkgtype in ['bin', 'lib', 'doc', 'src']:
                scriptName = "post-install-%s-%s.cmd" % (self.package, pkgtype)
                script = os.path.join(self.mergeDestinationDir(), "manifest", scriptName)
                if os.path.exists(script):
                    craftDebug.log.debug("run post install script '%s'" % script)
                    cmd = "cd /D %s && %s" % (self.mergeDestinationDir(), script)
                    if not utils.system(cmd):
                        craftDebug.log.warning("%s failed!" % cmd)
                else:
                    craftDebug.log.debug("post install script '%s' not found" % script)
        else:
            craftDebug.log.debug("running of post install scripts disabled!")

        # add package to installed database -> is this not the task of the manifest files ?

        revision = self.sourceRevision()
        package = installdb.addInstalled(self.package, self.version, revision=revision)
        fileList = self.getFileListFromDirectory(self.mergeDestinationDir(), copiedFiles)
        package.addFiles(fileList)
        package.install()

        return True

    def unmerge(self):
        """unmergeing the files from the filesystem"""
        craftDebug.log.debug("Packagebase unmerge called")

        ## \todo mergeDestinationDir() reads the real used merge dir from the
        ## package definition, which fails if this is changed
        ## a better solution will be to save the merge sub dir into
        ## /etc/portage/installed and to read from it on unmerge
        craftDebug.log.debug("unmerge package from %s" % self.mergeDestinationDir())
        packageList = installdb.getInstalledPackages(self.package)

        for package in packageList:
            fileList = package.getFilesWithHashes()
            self.unmergeFileList(self.mergeDestinationDir(), fileList, self.forced)
            package.uninstall()

        # run post-uninstall scripts
        if not craftSettings.getboolean("General", "EMERGE_NO_POST_INSTALL", False):
            for pkgtype in ['bin', 'lib', 'doc', 'src']:
                scriptName = "post-uninstall-%s-%s.cmd" % (self.package, pkgtype)
                script = os.path.join(self.mergeDestinationDir(), "manifest", scriptName)
                if os.path.exists(script):
                    craftDebug.log.debug("run post uninstall script '%s'" % script)
                    cmd = "cd /D %s && %s" % (self.mergeDestinationDir(), script)
                    if not utils.system(cmd):
                        craftDebug.log.warning("%s failed!" % cmd)
                else:
                    craftDebug.log.debug("post uninstall script '%s' not found" % script)
        else:
            craftDebug.log.debug("running of post uninstall scripts disabled!")

        return True

    def cleanImage(self) -> bool:
        """cleanup before install to imagedir"""
        if (os.path.exists(self.imageDir())):
            craftDebug.log.debug("cleaning image dir: %s" % self.imageDir())
            utils.cleanDirectory(self.imageDir())
            os.rmdir(self.imageDir())
        return True

    def cleanBuild(self) -> bool:
        """cleanup currently used build dir"""
        if os.path.exists(self.buildDir()):
            utils.cleanDirectory(self.buildDir())
            craftDebug.log.debug("cleaning build dir: %s" % self.buildDir())

        return True

    def stripLibs(self, pkgName):
        """strip debugging informations from shared libraries - mingw only!!! """
        return self.strip(pkgName + ".dll")

    def strip(self, fileName):
        """strip debugging informations from shared libraries and executables - mingw only!!! """
        if self.subinfo.options.package.disableStriping or not craftCompiler.isMinGW():
            craftDebug.log.debug("Skiping stipping of " + fileName)
            return True
        basepath = os.path.join(self.installDir())
        filepath = os.path.join(basepath, "bin", fileName)

        cmd = "strip -s " + filepath
        craftDebug.log.debug(cmd)
        os.system(cmd)
        return True

    def createImportLibs(self, pkgName):
        """create the import libraries for the other compiler(if ANSI-C libs)"""
        basepath = os.path.join(self.installDir())
        utils.createImportLibs(pkgName, basepath)

    def printFiles(self):
        packageList = installdb.getInstalledPackages(self.package)
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

        craftDebug.log.debug("PackageBase.execute called. args: %s" % sys.argv)
        command, _ = self.getAction(cmd)

        if self.subinfo.options.disableReleaseBuild and self.buildType() == "Release" \
                or self.subinfo.options.disableDebugBuild and self.buildType() == "Debug":
            print("target ignored for this build type")
            return False

        return self.runAction(command)

    def fetchBinary(self) -> bool:
        if self.subinfo.options.package.disableBinaryCache:
            return False

        archiveName = self.binaryArchiveName(includePackagePath=True)
        archvieFolder, localArchiveName = self.binaryArchiveName(includePackagePath=True).rsplit("/", 1)
        downloadFolder = os.path.join(self.cacheLocation(), archvieFolder)
        print(downloadFolder)

        if not os.path.exists(downloadFolder):
            os.makedirs(downloadFolder)

        for url in [self.cacheLocation()] + self.cacheRepositoryUrls():
            craftDebug.log.debug(f"Trying to restore {archiveName} from cache: {url}.")
            cache = utils.utilsCache.cacheJsonFromUrl(f"{url}/manifest.json")
            if not cache or not str(self) in cache or not archiveName in cache[str(self)]:
                continue
            if url != self.cacheLocation():
                if not os.path.exists(os.path.join(downloadFolder, localArchiveName)):
                    if not utils.getFile(f"{url}/{archiveName}", downloadFolder, localArchiveName):
                        return False
            return CraftHash.checkFilesDigests(downloadFolder, [localArchiveName],
                                               digests=cache[str(self)][archiveName]["checksum"],
                                               digestAlgorithm=CraftHash.HashAlgorithm.SHA256) and \
                   self.cleanImage() \
                   and utils.unpackFile(downloadFolder, localArchiveName, self.imageDir()) \
                   and self.qmerge()
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
    def unmergeFileList(rootdir, fileList, forced=False):
        """ delete files in the fileList if has matches or forced is True """
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
                    if forced:
                        craftDebug.log.warning("file %s has different hash: %s %s, deleting anyway" % \
                                               (fullPath, currentHash, filehash))
                        OsUtils.rm(fullPath, True)
                    else:
                        craftDebug.log.warning(
                            "file %s has different hash: %s %s, run with option --force to delete it anyway" % \
                            (fullPath, currentHash, filehash))
            elif not os.path.isdir(fullPath):
                craftDebug.log.warning("file %s does not exist" % fullPath)

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
                     "geturls": "getUrls",
                     "print-revision": "printSourceVersion",
                     "print-files": "printFiles",
                     "checkdigest": "checkDigest",
                     "fetch-binary": "fetchBinary"}
        if command in functions:
            try:
                ok = getattr(self, functions[command])()
            except AttributeError as e:
                raise PortageException(str(e), self.package, e)

        else:
            ok = craftDebug.log.error("command %s not understood" % command)

        return ok
