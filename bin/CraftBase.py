#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import datetime
import functools
import sys

import info
import utils
from CraftConfig import *
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Blueprints import CraftPackageObject
from CraftDebug import deprecated
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils.CraftShortPath import CraftShortPath
from CraftOS.osutils import OsUtils

class InitGuard(object):
    _initialized = {}
    _verbose = False

    @staticmethod
    def _dummy_init(key, *args, **kwargs):
        if InitGuard._verbose:
            print("dummy_init", key)
        args[0].__dict__ = InitGuard._initialized[key].__dict__

    @staticmethod
    def init_once(fun):
        @functools.wraps(fun)
        def inner(*args, **kwargs):
            if fun.__name__ != "__init__":
                raise Exception("InitGuard can only handle __init__ calls")
            key = (args[0].__class__, fun.__code__)
            if key not in InitGuard._initialized:
                if InitGuard._verbose:
                    print("init", key)
                InitGuard._initialized[key] = args[0]
                return fun(*args, **kwargs)
            else:
                return InitGuard._dummy_init(key, *args, **kwargs)

        return inner


class CraftBase(object):
    """base class for craft system - holds attributes and methods required by base classes"""

    @InitGuard.init_once
    def __init__(self):
        # TODO: some __init__  of subclasses need to already have been
        # called here. That is really the wrong way round.
        object.__init__(self)
        CraftCore.log.debug("CraftBase.__init__ called")

        mod = sys.modules[self.__module__]
        # ugly workaround we need to replace the constructor
        self.package = mod.CRAFT_CURRENT_MODULE  # type: CraftPackageObject
        self.subinfo = mod.subinfo(self) # type: info.infoclass

        self.buildSystemType = None

    def __str__(self):
        return self.package.__str__()

    @property
    def noFetch(self):
        return CraftCore.settings.getboolean("General", "WorkOffline", False)

    @property
    def buildTests(self):
        return self.subinfo.options.dynamic.buildTests

    def buildType(self):
        """return currently selected build type"""
        return self.subinfo.options.dynamic.buildType

    def buildArchitecture(self):
        """return the target CPU architecture"""
        CraftCore.compiler.architecture()

    def imageDirPattern(self):
        """return base directory name for package related image directory"""
        return f"image-{self.buildType()}-{self.buildTarget}"

    def sourceDir(self, dummyIndex=0):
        utils.abstract()

    def packageDir(self):
        """ add documentation """
        return os.path.dirname(self.package.source)

    def installPrefix(self):
        prefix = CraftCore.standardDirs.craftRoot()
        if self.buildTarget in self.subinfo.targetInstallPath:
            prefix = os.path.join(prefix, self.subinfo.targetInstallPath[self.buildTarget])
        return prefix

    def buildRoot(self):
        """return absolute path to the root directory of the currently active package"""
        return os.path.normpath(os.path.join(CraftStandardDirs.craftRoot(), "build", self.package.path))

    def workDir(self):
        """return absolute path to the 'work' subdirectory of the currently active package"""
        work = os.path.join(self.buildRoot(), "work")
        return CraftShortPath(work).shortPath

    def buildDir(self):
        if not self.subinfo.options.useShadowBuild:
            return self.sourceDir()
        CraftCore.log.debug("CraftBase.buildDir() called")
        builddir = os.path.join(self.workDir(), "build")
        CraftCore.log.debug(f"package builddir is: {builddir}")
        return builddir

    def imageDir(self):
        """return absolute path to the install root directory of the currently active package
        """
        return os.path.join(self.buildRoot(), self.imageDirPattern())

    def installDir(self):
        """return absolute path to the install directory of the currently active package.
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath is used
        """
        if self.subinfo.hasInstallPath():
            installDir = os.path.join(self.imageDir(), self.subinfo.installPath())
        else:
            installDir = self.imageDir()
        return installDir

    def packageDestinationDir(self):
        """return absolute path to the directory where binary packages are placed into.
        Default is to optionally append build type subdirectory"""

        CraftCore.log.debug("CraftBase.packageDestinationDir called")
        dstpath = CraftCore.settings.get("Packager", "Destination", os.path.join(CraftStandardDirs.craftRoot(), "tmp"))

        if not os.path.exists(dstpath):
            utils.createDir(dstpath)
        return dstpath

    @property
    def buildTarget(self):
        return self.subinfo.buildTarget

    @property
    def version(self):
        ver = self.subinfo.buildTarget
        patchLevel = 0
        if CraftCore.settings.getboolean("BlueprintVersions", "EnableDailyUpdates", True)\
                and self.subinfo.options.dailyUpdate and self.subinfo.hasSvnTarget():
            ver += "-" + str(datetime.date.today()).replace("-", ".")
        elif self.subinfo.options.dynamic.patchLevel:
            patchLevel = int(self.subinfo.options.dynamic.patchLevel)
        elif self.subinfo.buildTarget in self.subinfo.patchLevel:
            patchLevel = int(self.subinfo.patchLevel[self.subinfo.buildTarget])
        patchLevel += self.package.categoryInfo.patchLevel
        if patchLevel != 0:
            ver = f"{ver}-{patchLevel}"
        return ver

    @property
    def rootdir(self):
        return CraftStandardDirs.craftRoot()

    def enterBuildDir(self):
        CraftCore.debug.trace("CraftBase.enterBuildDir called")
        utils.createDir(self.buildDir())

        os.chdir(self.buildDir())
        CraftCore.log.debug("entering: %s" % self.buildDir())

    def enterSourceDir(self):
        if (not os.path.exists(self.sourceDir())):
            return False
        CraftCore.log.warning("entering the source directory!")
        os.chdir(self.sourceDir())
        CraftCore.log.debug("entering: %s" % self.sourceDir())

    def buildNumber(self):
        if "APPVEYOR_BUILD_VERSION" in os.environ:
            return os.environ["APPVEYOR_BUILD_VERSION"]
        elif "BUILD_NUMBER" in os.environ:
            return os.environ["BUILD_NUMBER"]
        return ""


    def binaryArchiveBaseName(self, pkgSuffix, includeRevision, includeTimeStamp) -> str:
        if not pkgSuffix:
            pkgSuffix = ""
            if hasattr(self.subinfo.options.package, 'packageSuffix') and self.subinfo.options.package.packageSuffix:
                pkgSuffix = self.subinfo.options.package.packageSuffix
        buildVersion = self.buildNumber()

        version = []
        if not buildVersion and self.subinfo.hasSvnTarget():
            if includeRevision:
                version += [self.sourceRevision(), self.version]
            else:
                version += ["latest", self.version]
        else:
            version += [self.version, buildVersion]
        if includeTimeStamp:
            version += [datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")]
        version = "-".join(filter(None, version))
        version = version.replace("/", "_")

        return f"{self.package.name}-{version}-{CraftCore.compiler}{pkgSuffix}"

    def binaryArchiveName(self, pkgSuffix=None, fileType=CraftCore.settings.get("Packager", "7ZipArchiveType", "7z"),
                          includeRevision=False, includePackagePath=False, includeTimeStamp=False) -> str:

        archiveBaseName = self.binaryArchiveBaseName(pkgSuffix, includeRevision, includeTimeStamp)

        if fileType:
            if not fileType.startswith("."):
                fileType = f".{fileType}"
        else:
            fileType = ""
        prefix = "" if not includePackagePath else f"{self.package.path}/"
        return f"{prefix}{archiveBaseName}{fileType}"


    @staticmethod
    def cacheVersion():
        if CraftCore.settings.getboolean("QtSDK", "Enabled", "False"):
            version = CraftCore.settings.get("QtSDK", "Version")
            return f"QtSDK_{version}"
        else:
            return CraftCore.settings.get("Packager", "CacheVersion")

    def cacheLocation(self, baseDir=None) -> str:
        if not baseDir:
            cacheDir = CraftCore.settings.get("Packager", "CacheDir", os.path.join(CraftStandardDirs.downloadDir(), "binary"))
        else:
            cacheDir = baseDir

        version = self.cacheVersion()
        if not version:
            return None
        return os.path.join(cacheDir, version, *CraftCore.compiler.signature, self.buildType())

    def cacheRepositoryUrls(self) -> [str]:
        version = self.cacheVersion()
        buildType = [self.buildType()]
        if self.buildType() == "RelWithDebInfo":
            buildType += ["Release"]
        elif self.buildType() == "Release":
            buildType += ["RelWithDebInfo"]
        out = []
        for bt in buildType:
            out += ["/".join([url if not url.endswith("/") else url[0:-1], version, *CraftCore.compiler.signature, bt]) for url in CraftCore.settings.getList("Packager", "RepositoryUrl")]
        return out

    def internalPostInstall(self):
        return True

    def postInstall(self):
        return True

    def internalPostQmerge(self):
        return True

    def postQmerge(self):
        return True

    def cleanImage(self) -> bool:
        """cleanup before install to imagedir"""
        if os.path.exists(self.imageDir()):
            return utils.cleanDirectory(self.imageDir())
        return True

    def cleanBuild(self) -> bool:
        """cleanup currently used build dir"""
        if not self.subinfo.options.useShadowBuild:
            return True
        if os.path.exists(self.buildDir()):
            return utils.cleanDirectory(self.buildDir())
        return True