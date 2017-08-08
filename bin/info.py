##
#
# @package  this module contains the information class

# the current work here is to access members only
# by methods to be able to separate the access from
# the definition

import datetime

import CraftHash
import VersionInfo
from options import *


class infoclass(object):
    """this module contains the information class"""

    def __init__(self, parent, optionList=[]):
        ### package options
        self.parent = parent
        self.options = Options(optionList)
        self.versionInfo = VersionInfo.VersionInfo(self)
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
        self.targetDigestUrls = {}
        ## \todo prelimary
        self.svnTargets = {}

        # runtimeDependencies and buildDependencies are not different when looking
        # at the build process itself, they will only make a difference when getting
        # output of the dependencies
        self.runtimeDependencies = {}
        self.buildDependencies = {}

        # a long and a short description for the package
        self.description = ""
        self.tags = ""
        # a url to the projects webpage
        self.webpage = ""

        self.patchToApply = {}  # key: target. Value: list(['patchname', patchdepth]) or ('patchname',patchdepth)
        self.svnTargets = {}
        self.svnServer = None  # this will result in the use of the default server (either anonsvn.kde.org or svn.kde.org)
        self._defaultTarget = None
        self.buildTarget = ""
        self.setTargets()
        self.setBuildTarget()
        self.setBuildOptions()

        # do this after buildTarget is set so that some dependencies can be set depending on self.buildTarget
        self.setDependencies()

    @property
    def package(self) -> str:
        return self.parent

    @property
    def defaultTarget(self) -> str:
        target = None
        if ("PortageVersions", self.package.package.path) in craftSettings:
            target = craftSettings.get("PortageVersions", self.package.package.path)
        if target in self.targets or target in self.svnTargets:
            return target
        return self._defaultTarget

    @defaultTarget.setter
    def defaultTarget(self, value):
        self._defaultTarget = value

    def setDependencies(self):
        """default method for setting dependencies, override to set individual targets"""

    def setTargets(self):
        """default method for setting targets, override to set individual targets"""

    def setBuildTarget(self, buildTarget=None):
        """setup current build target"""
        self.buildTarget = self.defaultTarget
        if not buildTarget == None:
            self.buildTarget = buildTarget
        if not self.buildTarget in self.targets and not self.buildTarget in self.svnTargets:
            self.buildTarget = self.defaultTarget

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
            return self.archiveNames[self.buildTarget]
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
        if (self.hasTarget() or self.hasSvnTarget()) \
                and self.buildTarget in self.targetSrcSuffix:
            return self.targetSrcSuffix[self.buildTarget]

    def hasTargetSourcePath(self) -> bool:
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.hasTarget() or self.hasSvnTarget()) \
               and self.buildTarget in self.targetInstSrc

    def targetSourcePath(self) -> str:
        """return relative path appendable to local source path for the recent target"""
        if (self.hasTarget() or self.hasSvnTarget()) \
                and self.buildTarget in self.targetInstSrc:
            return self.targetInstSrc[self.buildTarget]

    def hasConfigurePath(self) -> bool:
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.hasTarget() or self.hasSvnTarget()) \
               and self.buildTarget in self.targetConfigurePath

    def configurePath(self) -> str:
        """return relative path appendable to local source path for the recent target"""
        if (self.hasTarget() or self.hasSvnTarget()) and \
                        self.buildTarget in self.targetConfigurePath:
            return self.targetConfigurePath[self.buildTarget]

    def hasInstallPath(self) -> bool:
        """return true if relative path appendable to local install path is given for the recent target"""
        return (self.hasTarget() or self.hasSvnTarget()) \
               and self.buildTarget in self.targetInstallPath

    def installPath(self) -> str:
        """return relative path appendable to local install path for the recent target"""
        if (self.hasTarget() or self.hasSvnTarget()) \
                and self.buildTarget in self.targetInstallPath:
            return self.targetInstallPath[self.buildTarget]
        craftDebug.log.critical("no install path for this build target defined")

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
        return (self.hasTarget() or self.hasSvnTarget()) \
               and self.buildTarget in self.targetDigests

    def targetDigest(self) -> ([str], CraftHash.HashAlgorithm):
        """return digest(s) for the recent build target. The return value could be a string or a list"""
        if self.hasTargetDigests():
            out = self.targetDigests[self.buildTarget]
            if type(out) == str:
                out = [out]
            if not type(out) == tuple:
                out = (out, CraftHash.HashAlgorithm.SHA1)
            return out
        return None

    def hasTargetDigestUrls(self) -> bool:
        """return state if target has digest url(s) for the recent build target"""
        return (self.hasTarget() or self.hasSvnTarget()) \
               and self.buildTarget in self.targetDigestUrls

    def targetDigestUrl(self) -> ([str], CraftHash.HashAlgorithm):
        """return digest url(s) for the recent build target.  The return value could be a string or a list"""
        if self.hasTargetDigestUrls():
            out = self.targetDigestUrls[self.buildTarget]
            if type(out) == str:
                out = [out]
            if not type(out) == tuple:
                out = (out, CraftHash.HashAlgorithm.getAlgorithmFromFile(out[0]))
            return out
        return None
