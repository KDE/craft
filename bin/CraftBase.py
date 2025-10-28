#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import abc
import datetime
import functools
import json
import os
from pathlib import Path
from urllib.request import urlopen

import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore
from CraftDebug import deprecated
from CraftStandardDirs import CraftStandardDirs
from Utils.CraftShortPath import CraftShortPath


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
    def __init__(self, package: CraftPackageObject):
        # TODO: some __init__  of subclasses need to already have been
        # called here. That is really the wrong way round.
        object.__init__(self)
        CraftCore.log.debug("CraftBase.__init__ called")

        # ugly workaround we need to replace the constructor
        self.package = package
        self.subinfo: info.infoclass = self.package._Module.subinfo(self)

        self.buildSystemType = None

        self._latestVersion = None

    def __str__(self):
        return self.package.__str__()

    @property
    def noFetch(self):
        return CraftCore.settings.getboolean("General", "WorkOffline", False)

    @property
    def buildTests(self):
        return self.subinfo.options.dynamic.buildTests

    @property
    def latestVersion(self):
        if self._latestVersion:
            return self._latestVersion

        if not self.subinfo.releaseManagerId:
            CraftCore.log.warning("Release Manager ID is None.")
            return None

        with urlopen(f"https://release-monitoring.org/api/v2/versions/?project_id={self.subinfo.releaseManagerId}") as response:
            if response.status != 200:
                CraftCore.log.warning("Failed to fetch latest version.")
                return None

            data = json.loads(response.read().decode("utf-8"))
            self._latestVersion = data["latest_version"]
            return self._latestVersion

    @property
    def releaseMonitorUpdateAvailable(self):
        if self.latestVersion:
            return (CraftVersion(self.latestVersion) > CraftVersion(self.version))
        return False

    def buildType(self):
        """return currently selected build type"""
        return self.subinfo.options.dynamic.buildType

    def imageDirPattern(self):
        """return base directory name for package related image directory"""
        return f"image-{self.buildType()}-{self.buildTarget.replace('/', '_') if self.buildTarget else None}"

    @abc.abstractmethod
    def sourceDir(self, dummyIndex=0) -> Path:
        pass

    def logDir(self) -> Path:
        return CraftCore.standardDirs.logDir() / self.package.path

    def blueprintDir(self):
        """The folder containing this blueprint"""
        return Path(self.package.source).parent

    @deprecated("self.blueprintDir()")
    def packageDir(self) -> Path:
        return self.blueprintDir()

    def installPrefix(self) -> Path:
        prefix = Path(CraftCore.standardDirs.craftRoot())
        if self.buildTarget in self.subinfo.targetInstallPath:
            prefix = prefix / self.subinfo.targetInstallPath[self.buildTarget]
        return prefix

    def buildRoot(self) -> Path:
        """return absolute path to the root directory of the currently active package"""
        return CraftStandardDirs.craftRoot() / "build" / self.package.path

    def workDir(self) -> Path:
        """return absolute path to the 'work' subdirectory of the currently active package"""
        return Path(CraftShortPath(self.buildRoot() / "work").shortPath)

    def buildDir(self) -> Path:
        if not self.subinfo.options.useShadowBuild:
            return self.sourceDir()
        CraftCore.log.debug("CraftBase.buildDir() called")
        builddir = self.workDir() / "build"
        CraftCore.log.debug(f"package builddir is: {builddir}")
        return builddir

    def imageDir(self) -> Path:
        """return absolute path to the install root directory of the currently active package"""
        return CraftShortPath(self.buildRoot()).shortPath / self.imageDirPattern()

    def installDir(self) -> Path:
        """return absolute path to the install directory of the currently active package.
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath is used
        """
        if self.subinfo.hasInstallPath():
            return self.imageDir() / self.subinfo.installPath()
        else:
            return self.imageDir()

    def packageDestinationDir(self) -> Path:
        """return absolute path to the directory where binary packages are placed into.
        Default is to optionally append build type subdirectory"""

        CraftCore.log.debug("CraftBase.packageDestinationDir called")
        dstpath = Path(
            CraftCore.settings.get(
                "Packager",
                "Destination",
                CraftCore.standardDirs.tmpDir(),
            )
        ).resolve()
        utils.createDir(dstpath)
        return dstpath

    def symbolsImageDir(self) -> Path:
        return self.buildRoot() / f"{self.imageDirPattern()}-dbg"

    @property
    def buildTarget(self):
        return self.subinfo.buildTarget

    @property
    def version(self):
        ver = self.subinfo.buildTarget
        patchLevel = 0
        if CraftCore.settings.getboolean("BlueprintVersions", "EnableDailyUpdates", True) and self.subinfo.options.dailyUpdate and self.subinfo.hasSvnTarget():
            ver += "-" + str(datetime.date.today()).replace("-", ".")
        elif self.subinfo.buildTarget in self.subinfo.patchLevel:
            patchLevel = int(self.subinfo.patchLevel[self.subinfo.buildTarget])
        if self.subinfo.options.dynamic.patchLevel:
            patchLevel += int(self.subinfo.options.dynamic.patchLevel)
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
        if not self.sourceDir().is_dir():
            return False
        CraftCore.log.warning("entering the source directory!")
        os.chdir(self.sourceDir())
        CraftCore.log.debug("entering: %s" % self.sourceDir())

    def buildNumber(self):
        return (
            os.environ.get("APPVEYOR_BUILD_VERSION")
            or os.environ.get("BUILD_NUMBER")
            or os.environ.get("DRONE_BUILD_NUMBER")
            or os.environ.get("CI_PIPELINE_IID")
            or ""
        )

    def formatVersion(self, includeRevision, includeTimeStamp) -> str:
        buildVersion = self.buildNumber()

        version = []
        if not buildVersion and self.subinfo.hasSvnTarget():
            if includeRevision:
                version += [self.sourceRevision(), self.version]
            else:
                version += ["latest", self.version]
        else:
            if self.subinfo.options.dynamic.srcDir:
                version += [self.sourceRevision()]
            else:
                version += [self.version]
            version += [buildVersion]
        if includeTimeStamp:
            version += [datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S")]
        version = "-".join(filter(None, version))
        return version.replace("/", "_")

    def binaryArchiveBaseName(self, pkgSuffix, includeRevision, includeTimeStamp) -> str:
        return f"{self.package.name}-{self.formatVersion(includeRevision=includeRevision, includeTimeStamp=includeTimeStamp)}-{CraftCore.compiler}{pkgSuffix}"

    def binaryArchiveName(
        self,
        pkgSuffix="",
        fileType=CraftCore.settings.get("Packager", "7ZipArchiveType", "7z"),
        includeRevision=False,
        includePackagePath=False,
        includeTimeStamp=False,
    ) -> str:
        archiveBaseName = self.binaryArchiveBaseName(pkgSuffix, includeRevision, includeTimeStamp)

        if fileType:
            if not fileType.startswith("."):
                fileType = f".{fileType}"
            if fileType == ".7z" and not CraftCore.cache.findApplication("7za"):
                # we are bootstrapping and can't use 7z yet
                if CraftCore.compiler.isUnix:
                    fileType = ".xz"
                else:
                    fileType = ".zip"
        else:
            fileType = ""
        prefix = "" if not includePackagePath else f"{self.package.path}/"
        return f"{prefix}{archiveBaseName}{fileType}"

    @staticmethod
    def cacheVersion():
        return CraftCore.settings.get("Packager", "CacheVersion")

    def cacheLocation(self, baseDir=None) -> Path:
        if not baseDir:
            cacheDir = Path(
                CraftCore.settings.get(
                    "Packager",
                    "CacheDir",
                    os.path.join(CraftStandardDirs.downloadDir(), "binary"),
                )
            ).resolve()
        else:
            cacheDir = Path(baseDir)

        version = self.cacheVersion()
        if not version:
            return None
        return Path(os.path.join(cacheDir, version, *CraftCore.compiler.signature, self.buildType()))

    def cacheRepositoryUrls(self) -> list[str]:
        buildType = [self.buildType()]
        if self.buildType() == "RelWithDebInfo":
            buildType += ["Release"]
        elif self.buildType() == "Release":
            buildType += ["RelWithDebInfo"]
        out = []
        for bt in buildType:
            out += [
                "/".join(
                    [
                        url,
                        bt,
                    ]
                )
                for url in CraftCore.settings.cacheRepositoryUrls()
            ]
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
