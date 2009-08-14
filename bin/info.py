## 
#
# @package  this module contains the information class

# the current work here is to access members only 
# by methods to be able to separate the access from 
# the definition 

import datetime
import os
import utils

## options for the configure action 
class OptionsConfigure:
    def __init__(self):
        ## with this option additional definitions could be added to the configure commmand line
        self.defines = None
        ## set source subdirectory as source root for the configuration tool.
        # Sometimes it is required to take a subdirectory from the source tree as source root 
        # directory for the configure tool, which could be enabled by this option. The value of
        # this option is added to sourceDir() and the result is used as source root directory. 
        self.configurePath = None
        # add build target to be included into build. This feature is cmake only and requires the 
        # usage of the 'macro_optional_add_subdirectory' macro. The value is a string.
        self.onlyBuildTargets = None 

## options for the make action 
class OptionsMake:
    def __init__(self):
        ## ignore make error 
        self.ignoreErrors = None
        ## options for the make tool
        self.makeOptions = None

## options for the install action 
class OptionsInstall:
    def __init__(self):
        ## use either make tool for installing or 
        # run cmake directly for installing 
        self.useMakeToolForInstall = True

## options for the merge action 
class OptionsMerge:
    def __init__(self):
        ## subdir based on installDir() used as merge source directory
        self.sourcePath = None
        ## subdir based on mergeDir() used as  merge destination directory
        self.destinationPath = None
        ## merge/unmerge the package build type independent 
        # this option is ignored when the environment variable 
        # EMERGE_MERGE_ROOT_WITH_BUILD_TYPE is not set or is false
        self.ignoreBuildType = False
        
## options for the package action 
class OptionsPackage:
    def __init__(self):
        ## defines the package name 
        self.packageName = None
        ## defines the package version 
        self.version = None
        ## use compiler in package name
        self.withCompiler = True
        ## use special packaging mode  (only for qt)
        self.specialMode = False
        ## pack also sources 
        self.packSources = True
        
## main option class
class Options:
    def __init__(self):
        ## options of the configure action
        self.configure = OptionsConfigure()
        ## options of the configure action
        self.make = OptionsMake()
        ## options of the install action
        self.install = OptionsInstall()
        ## options of the package action
        self.package = OptionsPackage()
        ## options of the merge action
        self.merge = OptionsMerge()
        
        ## this option controls if the build type is used when creating build and install directories. 
        # The following example shows the difference:
        # \code
        #                True                                False
        # work/msvc2008-RelWithDebInfo-svnHEAD     work/msvc2008-svnHEAD  
        # image-msvc2008-RelWithDebInfo-svnHEAD    image-msvc2008-svnHEAD
        # \endcode
        #
        self.useBuildType = True
        
        ## this option controls if the active compiler is used when creating build and install directories. 
        # The following example shows the difference:
        # \code 
        #               True                                  False
        # work/msvc2008-RelWithDebInfo-svnHEAD     work/RelWithDebInfo-svnHEAD
        # image-msvc2008-RelWithDebInfo-svnHEAD    image-RelWithDebInfo-svnHEAD
        # \endcode
        #
        self.useCompilerType = True
        ## skip the related package from debug builds
        self.disableDebugBuild = False
        ## skip the related package from release builds
        self.disableReleaseBuild = False
        ## exit if system command returns errors
        self.exitOnErrors = True

class infoclass:
    def __init__( self, RAW="" ):
        """ """
        ### package options
        self.options = Options()
        self.targets = dict()
        self.targetInstSrc = dict()
        self.targetConfigurePath = dict()
        self.targetInstallPath = dict()
        self.targetMergeSourcePath = dict()
        self.targetMergePath = dict()
        ## \todo prelimary 
        self.svnTargets = dict()
        self.hardDependencies = dict()
        self.softDependencies = dict()
        self.patchToApply = dict()  # list ( 'patchname', patchdepth for patch )
        self.isoDateToday = str( datetime.date.today() ).replace('-', '')
        self.svnTargets['svnHEAD'] = False
        self.svnServer = None       # this will result in the use of the default server (either anonsvn.kde.org or svn.kde.org)
        self.defaultTarget = 'svnHEAD'
        self.buildTarget = 'svnHEAD'
        
        for x in RAW.splitlines():
            if not x == '':
                """ if version is not available then set it as -1 """
                self.hardDependencies[ x ] = [ -1 ]
        

        self.setDependencies()
        self.setTargets()
        self.setSVNTargets()
        self.setBuildTarget()

    # abstract method for setting dependencies, override to set individual targets
    def setDependencies( self ):
        """ """

    # abstract method for setting targets, override to set individual targets
    def setTargets( self ):
        """ """

    # abstract method for setting svn targets, override to set individual targets
    def setSVNTargets( self ):
        """ """
    
    # setup current build target 
    def setBuildTarget( self, buildTarget = None):
        self.buildTarget = self.defaultTarget
        if not buildTarget == None:
            self.buildTarget = buildTarget
        elif not os.getenv( "EMERGE_TARGET" ) == None:
            self.buildTarget = os.getenv( "EMERGE_TARGET" )
        if not self.buildTarget in self.targets.keys() and not self.buildTarget in self.svnTargets.keys() :
            self.buildTarget = self.defaultTarget
            utils.debug("build target %s not defined in available targets %s %s" % (self.buildTarget, self.targets.keys(), self.svnTargets.keys()), 1)
        else:
            utils.debug( "setting buildtarget to " + self.buildTarget, 2 )
    
    # return archive file based package url 
    def getPackage( self, repoUrl, name, version, ext='.tar.bz2' ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"
        elif os.getenv("KDECOMPILER") == "msvc2008":
            compiler = "vc90"

        return repoUrl + '/' + name + '-' + compiler + '-' + version + '-bin' + ext + '\n' + \
               repoUrl + '/' + name + '-' + compiler + '-' + version + '-lib' + ext + '\n'

    # return archive file based package url for unified packages
    def getUnifiedPackage( self, repoUrl, name, version, ext='.tar.bz2' ):
        return repoUrl + '/' + name + '-' + version + '-bin' + ext + '\n' + \
               repoUrl + '/' + name + '-' + version + '-lib' + ext + '\n'

    # return true if archive targets for the currently selected build target is available
    def hasTarget( self ):
        return self.buildTarget in self.targets.keys()
        
    # return archive target
    def target( self ):
        if self.buildTarget in self.targets.keys():
            return self.targets[self.buildTarget]
        return ""

    # return true if version system based target for the currently selected build target is available
    def hasSvnTarget( self ):
        return self.buildTarget in self.svnTargets.keys()
        
    # return version system based target for the currently selected build target
    def svnTarget( self ):
        if self.buildTarget in self.svnTargets.keys():
            return self.svnTargets[self.buildTarget]
        return ""

    def hasTargetSourcePath(self):
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetInstSrc.keys()
            
    def targetSourcePath(self):
        """return relative path appendable to local source path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetInstSrc.keys():
            return self.targetInstSrc[ self.buildTarget ]
        
    def hasConfigurePath(self):
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetConfigurePath.keys()
            
    def configurePath(self):
        """return relative path appendable to local source path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetConfigurePath.keys():
            return self.targetConfigurePath[ self.buildTarget ]

    def hasInstallPath(self):
        """return true if relative path appendable to local install path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetInstallPath.keys()
                
    def installPath(self):
        """return relative path appendable to local install path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetInstallPath.keys():
            return self.targetInstallPath[ self.buildTarget ]
        utils.die("no install path for this build target defined")
            
    def hasMergePath(self):
        """return true if relative path appendable to local merge path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetMergePath.keys()
                
    def mergePath(self):
        """return relative path appendable to local merge path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetMergePath.keys():
            return self.targetMergePath[ self.buildTarget ]

    def hasMergeSourcePath(self):
        """return true if relative path appendable to local merge source path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetMergeSourcePath.keys()
                
    def mergeSourcePath(self):
        """return relative path appendable to local merge source path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetMergeSourcePath.keys():
            return self.targetMergeSourcePath[ self.buildTarget ]

    def patchesToApply(self):
        """return patch informations for the recent build target"""
        if len( self.targets ) and self.buildTarget in self.patchToApply.keys():
            return self.patchToApply[ self.buildTarget ]
        return ("","")
