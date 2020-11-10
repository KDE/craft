##
#
# @package  this module contains the information class

# the current work here is to access members only
# by methods to be able to separate the access from
# the definition
from enum import Enum, unique

import VersionInfo
from Utils import CraftHash, CraftManifest
from options import *
from CraftDebug import deprecated


@unique
class DependencyRequirementType(Enum):
    Optional = 0
    Required = 1

class infoclass(object):
    """this module contains the information class"""

    def __init__(self, parent):
        ### package options
        self.parent = parent
        self.options = Options(parent.package)
        self.versionInfo = VersionInfo.VersionInfo(subinfo=self)
        # whethe we can add this blueprint to a shelve
        # blueprints that specify different versions for different platforms are not supported
        self.shelveAble = True
        self.targets = {}
        self.archiveNames = {}
        # Specifiy that the fetched source should be placed into a
        # subdirectory of the default source directory
        self.targetInstSrc = {}
        # Specifiy that the default source directory should have a suffix after
        # the package name. This is usefull for package which needs different sources.
        self.targetSrcSuffix = {}
        self.targetConfigurePath = {}
        self.targetInstallPath = {}

        self.targetDigests = {}
        self.targetDigestsX64 = {}
        self.targetDigestUrls = {}
        ## \todo prelimary
        self.svnTargets = {}
        self.targetUpdatedRepoUrl = {}

        self.patchLevel = {}

        # the build prefix, may differ for for cached files
        self.buildPrefix = CraftCore.standardDirs.craftRoot()
        self.isCachedBuild = False

        # runtimeDependencies and buildDependencies are not different when looking
        # at the build process itself, they will only make a difference when getting
        # output of the dependencies
        self.runtimeDependencies = {}
        self.buildDependencies = {}
        self.packagingDependencies = {}

        self.displayName = self.parent.package.name
        self.description = ""
        # tag words describing the package
        self.tags = ""
        # a url to the projects webpage
        self.webpage = ""

        self.patchToApply = {}  # key: target. Value: list(['patchname', patchdepth]) or ('patchname',patchdepth)
        self.svnTargets = {}
        self.svnServer = None  # this will result in the use of the default server (either anonsvn.kde.org or svn.kde.org)
        self._defaultTarget = None

        self.registerOptions()

        self.setTargets()
        self.setBuildOptions()

        # do this after buildTarget is set so that some dependencies can be set depending on self.buildTarget
        self.setDependencies()

    @property
    @deprecated("self.parent")
    def package(self):
        # -> PackageBase
        return self.parent

    @property
    def defaultTarget(self) -> str:
        target = self.options.dynamic.version
        # TODO: legacy behaviour
        if ("BlueprintVersions", self.parent.package.path) in CraftCore.settings:
            target = CraftCore.settings.get("BlueprintVersions", self.parent.package.path)
            CraftCore.log.warning(f"You are using the depreaced:\n"
                                f"[BlueprintVersions]\n"
                                f"{self.parent.package.path} = {target}\n\n"
                                f"Please use CraftOptions.ini\n"
                                f"[{self.parent.package.path}]\n"
                                f"version = {target}")
        if target:
            if target in self.targets or target in self.svnTargets:
                return target
            elif not self.parent.package.isIgnored():
                raise BlueprintException(f"You defined an invalid target {target} for {self.parent.package.path}, avaialble versions are {list(self.targets.keys()) + list(self.svnTargets.keys())} ", self.parent.package)
        return self._defaultTarget


    @defaultTarget.setter
    def defaultTarget(self, value):
        self._defaultTarget = value

    @property
    def buildTarget(self):
        return self.defaultTarget

    def registerOptions(self):
        """calls to self.options.dynamic.registerOption
        #self.options.dynamic.registerOption("fullKDevelop", False)
        """
        pass

    def setDependencies(self):
        """default method for setting dependencies, override to set individual targets"""

    def setTargets(self):
        """default method for setting targets, override to set individual targets"""

    def setBuildOptions(self):
        """default method for setting build options, override to set individual targets"""
        return

    def hasTarget(self) -> bool:
        """return true if archive targets for the currently selected build target is available"""
        return self.buildTarget in self.targets

    def target(self) -> str:
        """return archive target"""
        if self.buildTarget in self.targets:
            return self.targets[self.buildTarget]
        return ""

    def archiveName(self) -> [str]:
        """returns the archive file name"""
        if self.buildTarget in self.archiveNames:
            name = self.archiveNames[self.buildTarget]
            return name if isinstance(name, list) else [name]
        if type(self.targets[self.buildTarget]) == list:
            return [os.path.split(x)[-1] for x in self.targets[self.buildTarget]]
        else:
            return [os.path.split(self.targets[self.buildTarget])[-1]]

    def hasSvnTarget(self) -> bool:
        """return true if version system based target for the currently selected build target is available"""
        return self.buildTarget in self.svnTargets

    def svnTarget(self) -> str:
        """return version system based target for the currently selected build target"""
        if self.buildTarget in self.svnTargets:
            return self.svnTargets[self.buildTarget]
        return ""

    def targetSourceSuffix(self) -> str:
        """return local source path suffix for the recent target"""
        if self.buildTarget in self.targetSrcSuffix:
            return self.targetSrcSuffix[self.buildTarget]

    def hasTargetSourcePath(self) -> bool:
        """return true if relative path appendable to local source path is given for the recent target"""
        return self.buildTarget in self.targetInstSrc

    def targetSourcePath(self) -> str:
        """return relative path appendable to local source path for the recent target"""
        if self.buildTarget in self.targetInstSrc:
            return self.targetInstSrc[self.buildTarget]

    def hasConfigurePath(self) -> bool:
        """return true if relative path appendable to local source path is given for the recent target"""
        return self.buildTarget in self.targetConfigurePath

    def configurePath(self) -> str:
        """return relative path appendable to local source path for the recent target"""
        if (self.hasTarget() or self.hasSvnTarget()) and \
                        self.buildTarget in self.targetConfigurePath:
            return self.targetConfigurePath[self.buildTarget]

    def hasInstallPath(self) -> bool:
        """return true if relative path appendable to local install path is given for the recent target"""
        return self.buildTarget in self.targetInstallPath

    def installPath(self) -> str:
        """return relative path appendable to local install path for the recent target"""
        if self.buildTarget in self.targetInstallPath:
            return self.targetInstallPath[self.buildTarget]
        CraftCore.log.critical("no install path for this build target defined")

    def hasPatches(self) -> bool:
        """return state for having patches for the recent target"""
        return (self.hasTarget() or self.hasSvnTarget()) and self.buildTarget in self.patchToApply

    def patchesToApply(self) -> [tuple]:
        """return patch informations for the recent build target"""
        if self.hasPatches():
            out = self.patchToApply[self.buildTarget]
            return out if type(out) == list else [out]
        return [("", "")]

    def hasTargetDigests(self) -> bool:
        """return state if target has digest(s) for the recent build target"""
        if CraftCore.compiler.isX64() and self.buildTarget in self.targetDigestsX64:
            return True
        return self.buildTarget in self.targetDigests

    def targetDigest(self) -> ([str], CraftHash.HashAlgorithm):
        """return digest(s) for the recent build target. The return value could be a string or a list"""
        if self.hasTargetDigests():
            if CraftCore.compiler.isX64() and self.buildTarget in self.targetDigestsX64:
                out = self.targetDigestsX64[self.buildTarget]
            else:
                out = self.targetDigests[self.buildTarget]
            if type(out) == str:
                out = [out]
            if not type(out) == tuple:
                out = (out, CraftHash.HashAlgorithm.SHA1)
            return out
        return None

    def hasTargetDigestUrls(self) -> bool:
        """return state if target has digest url(s) for the recent build target"""
        return self.buildTarget in self.targetDigestUrls

    def targetDigestUrl(self) -> ([str], CraftHash.HashAlgorithm):
        """return digest url(s) for the recent build target.  The return value could be a string or a list"""
        if self.hasTargetDigestUrls():
            out = self.targetDigestUrls[self.buildTarget]
            if isinstance(out, str):
                out = [out]
            if not isinstance(out, tuple):
                out = (out, CraftHash.HashAlgorithm.getAlgorithmFromFile(out[0]))
            elif not isinstance(out[0], list):
                out = ([out[0]], out[1])
            return out
        return None

    def addCachedAutotoolsBuild(self, packageName=None, targetInstallPath=None):
        if not CraftCore.compiler.isMSVC():
            return
        self.versionInfo.setDefaultValues()
        if packageName:
            package = CraftPackageObject._allLeaves.get(packageName, None)
            if not package:
                raise BlueprintException(f"Failed to find {packageName}", package)
            packageName = package.path
            self.description = package.subinfo.description
        else:
            package = self.parent.package
            packageName = self.parent.package.path

        for key, url in list(self.targets.items()):
            if url.endswith("/"):
                url = url[:-1]
            json = CraftCore.cache.cacheJsonFromUrl(f"{url}/manifest.json")
            if not json:
                raise BlueprintException("Failed to load manifest", package)
                continue
            manifest = CraftManifest.CraftManifest.fromJson(json)
            if packageName not in manifest.packages[f"windows-mingw_{CraftCore.compiler.bits}-gcc"]:
                del self.targets[key]
                CraftCore.log.debug(f"Failed to find {packageName} on {url}")
                continue
            data = manifest.packages[f"windows-mingw_{CraftCore.compiler.bits}-gcc"][packageName].latest
            self.targets[key] = f"{url}/{data.fileName}"
            self.targetDigests[key] = ([data.checksum], CraftHash.HashAlgorithm.SHA256)
            if packageName != self.parent.package:
                if data.version in package.subinfo.patchLevel:
                    self.patchLevel[key] = package.subinfo.patchLevel[data.version]
            if targetInstallPath:
                self.targetInstallPath[key] = os.path.join(targetInstallPath, self.parent.package.name)


    def addCachedBuild(self, url, packageName = None, packagePath=None, targetInstallPath=None):
        if packageName:
            package = CraftPackageObject._allLeaves.get(packageName, None)
            if not package:
                raise BlueprintException(f"Failed to find {packageName}", package)
            packagePath = package.path
            self.description = package.subinfo.description
        elif not packagePath:
            packagePath = self.parent.package.path


        if url.endswith("/"):
                url = url[:-1]
        manifest = CraftManifest.CraftManifest.fromJson(CraftCore.cache.cacheJsonFromUrl(f"{url}/manifest.json"))
        latest = manifest.packages[f"windows-mingw_{CraftCore.compiler.bits}-gcc"][packagePath].latest
        self.targets[latest.version] = f"{url}/{latest.fileName}"
        self.targetDigests[latest.version] = ([latest.checksum], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = latest.version
        if targetInstallPath:
                self.targetInstallPath[latest.version] = os.path.join(targetInstallPath, self.parent.package.name)
