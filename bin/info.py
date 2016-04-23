##
#
# @package  this module contains the information class

# the current work here is to access members only
# by methods to be able to separate the access from
# the definition

import datetime
import os
from collections import OrderedDict

import EmergeDebug
import utils
import compiler
from options import *
import VersionInfo
import EmergeHash


class infoclass(object):
    """this module contains the information class"""
    def __init__( self, parent, optionList=[]):
        ### package options
        self.parent = parent
        self.options = Options(optionList)
        self.versionInfo = VersionInfo.VersionInfo(self)
        self.targets = OrderedDict()
        self.archiveNames = OrderedDict()
        # Specifiy that the fetched source should be placed into a
        # subdirectory of the default source directory
        self.targetInstSrc = OrderedDict()
        # Specifiy that the default source directory should have a suffix after
        # the package name. This is usefull for package which needs different sources.
        self.targetSrcSuffix = OrderedDict()
        self.targetConfigurePath = OrderedDict()
        self.targetInstallPath = OrderedDict()
        self.targetMergeSourcePath = OrderedDict()
        self.targetMergePath = OrderedDict()

        self.targetDigests = OrderedDict()
        self.targetDigestUrls = OrderedDict()
        ## \todo prelimary
        self.svnTargets = OrderedDict()


        # dependencies is the common way to define dependencies that are both
        # run time and build time dependencies,
        # runtimeDependencies and buildDependencies are not different when looking
        # at the build process itself, they will only make a difference when getting
        # output of the dependencies
        self.dependencies = OrderedDict()
        self.runtimeDependencies = OrderedDict()
        self.buildDependencies = OrderedDict()

        # a long and a short description for the package
        self.shortDescription = ''
        self.description = ''
        #a url to the projects homepage
        self.homepage = ''


        self.patchToApply = OrderedDict()  # key: target. Value: list(['patchname', patchdepth]) or ('patchname',patchdepth)
        self.isoDateToday = str( datetime.date.today() ).replace('-', '')
        self.svnTargets['svnHEAD'] = False
        self.svnServer = None       # this will result in the use of the default server (either anonsvn.kde.org or svn.kde.org)
        self._defaultTarget = None
        self.buildTarget = 'svnHEAD'
        self.setTargets()
        self.setBuildTarget()
        self.setBuildOptions()

        # do this after buildTarget is set so that some dependencies can be set depending on self.buildTarget
        self.setDependencies()

    @property
    def package(self) -> str:
        return self.parent.package

    @property
    def category(self) -> str:
        return self.parent.category

    @property
    def defaultTarget(self) -> str:
        target = None
        if ("PortageVersions", "%s/%s" % ( self.category, self.package )) in emergeSettings:
            target = emergeSettings.get("PortageVersions", "%s/%s" % ( self.category, self.package ))
        elif ("PortageVersions", "DefaultTarget") in emergeSettings:
            target = emergeSettings.get("PortageVersions", "DefaultTarget")
        if target in list(self.targets.keys()) or target in list(self.svnTargets.keys()) :
            return target
        return self._defaultTarget

    @defaultTarget.setter
    def defaultTarget(self, value):
        self._defaultTarget = value

    def setDependencies( self ):
        """default method for setting dependencies, override to set individual targets"""

    def setTargets( self ):
        """default method for setting targets, override to set individual targets"""

    def setBuildTarget( self, buildTarget = None):
        """setup current build target"""
        self.buildTarget = self.defaultTarget
        if not buildTarget == None:
            self.buildTarget = buildTarget
        if not self.buildTarget in list(self.targets.keys()) and not self.buildTarget in list(self.svnTargets.keys()) :
            self.buildTarget = self.defaultTarget

    def setBuildOptions( self ):
        """default method for setting build options, override to set individual targets"""
        return

    @staticmethod
    def getArchitecture() -> str:
        return "-%s" % compiler.architecture()

    def hasTarget( self ) -> bool:
        """return true if archive targets for the currently selected build target is available"""
        return self.buildTarget in list(self.targets.keys())

    def target( self ) -> str:
        """return archive target"""
        if self.buildTarget in list(self.targets.keys()):
            return self.targets[self.buildTarget]
        return ""

    def archiveName( self ) -> [str]:
        """returns the archive file name"""
        if self.buildTarget in list(self.archiveNames.keys()):
            return self.archiveNames[self.buildTarget]
        if type(self.targets[self.buildTarget]) == list:
            return [os.path.split(x)[-1] for x in self.targets[self.buildTarget] ]
        else:
            return [os.path.split(self.targets[self.buildTarget])[-1]]

    def hasMultipleTargets( self ) -> bool:
        """return whether we used a list of targets"""
        return type( self.targets[self.buildTarget] ) == list

    def targetCount( self ) -> int:
        """return the number of targets given either in a list, or split by a space character"""
        if self.hasMultipleTargets():
            return len( self.targets[self.buildTarget] )
        else:
            return len( self.targets[self.buildTarget].split() )

    def targetAt( self, index ) -> str:
        """return the specified target at a specific position, or an empty string if out of bounds"""
        if self.targetCount() <= index:
            return ""

        if self.hasMultipleTargets():
            return self.targets[self.buildTarget][index]
        else:
            return self.targets[self.buildTarget].split()[index]

    def hasSvnTarget( self ) -> bool:
        """return true if version system based target for the currently selected build target is available"""
        return self.buildTarget in list(self.svnTargets.keys())

    def svnTarget( self ) -> str:
        """return version system based target for the currently selected build target"""
        if self.buildTarget in list(self.svnTargets.keys()):
            return self.svnTargets[self.buildTarget]
        return ""

    def targetSourceSuffix(self) -> str:
        """return local source path suffix for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetSrcSuffix.keys()):
            return self.targetSrcSuffix[ self.buildTarget ]

    def hasTargetSourcePath(self) -> bool:
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetInstSrc.keys())

    def targetSourcePath(self) -> str:
        """return relative path appendable to local source path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetInstSrc.keys()):
            return self.targetInstSrc[ self.buildTarget ]

    def hasConfigurePath(self) -> bool:
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetConfigurePath.keys())

    def configurePath(self) -> str:
        """return relative path appendable to local source path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) and \
                self.buildTarget in list(self.targetConfigurePath.keys()):
            return self.targetConfigurePath[ self.buildTarget ]

    def hasInstallPath(self) -> bool:
        """return true if relative path appendable to local install path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetInstallPath.keys())

    def installPath(self) -> str:
        """return relative path appendable to local install path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetInstallPath.keys()):
            return self.targetInstallPath[ self.buildTarget ]
        EmergeDebug.die("no install path for this build target defined")

    def hasMergePath(self) -> bool:
        """return true if relative path appendable to local merge path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetMergePath.keys())

    def mergePath(self) -> str:
        """return relative path appendable to local merge path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetMergePath.keys()):
            return self.targetMergePath[ self.buildTarget ]

    def hasMergeSourcePath(self) -> bool:
        """return true if relative path appendable to local merge source path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetMergeSourcePath.keys())

    def mergeSourcePath(self) -> str:
        """return relative path appendable to local merge source path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetMergeSourcePath.keys()):
            return self.targetMergeSourcePath[ self.buildTarget ]

    def hasPatches(self) -> bool:
        """return state for having patches for the recent target"""
        return (len( self.targets ) or len( self.svnTargets )) and self.buildTarget in list(self.patchToApply.keys())

    def patchesToApply(self) -> [tuple]:
        """return patch informations for the recent build target"""
        if self.hasPatches():
            out = self.patchToApply[ self.buildTarget ]
            return out if type(out) == list else [out]
        return [("", "")]

    def hasTargetDigests(self) -> bool:
        """return state if target has digest(s) for the recent build target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetDigests.keys())

    def targetDigest(self) -> ([str], EmergeHash.HashAlgorithm):
        """return digest(s) for the recent build target. The return value could be a string or a list"""
        if self.hasTargetDigests():
            out = self.targetDigests[ self.buildTarget ]
            if type(out) == str:
                out = [out]
            if not type(out) == tuple:
                out = (out, EmergeHash.HashAlgorithm.SHA1)
            return out
        return None

    def hasTargetDigestUrls(self) -> bool:
        """return state if target has digest url(s) for the recent build target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetDigestUrls.keys())

    def targetDigestUrl(self) -> ([str], EmergeHash.HashAlgorithm):
        """return digest url(s) for the recent build target.  The return value could be a string or a list"""
        if self.hasTargetDigestUrls():
            out = self.targetDigestUrls[ self.buildTarget ]
            if type(out) == str:
                out = [out]
            if not type(out) == tuple:
                out = (out, EmergeHash.HashAlgorithm.SHA1)
            return out
        return None
        
        

   
