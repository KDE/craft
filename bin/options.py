## 
#
# @package  this module contains the option class
#

import os

## options for the fetch action 
class OptionsFetch:
    def __init__(self):
        ## option comment
        self.option = None
        
## options for the unpack action 
class OptionsUnpack:
    def __init__(self):
        ## By default archives are unpackaged into the workdir. 
        #  Use this option to unpack archives into recent build directory
        self.unpackIntoBuildDir = False
        
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
        
        # add the cmake defines that are needed to build tests here
        self.testDefine = None

## options for the make action 
class OptionsMake:
    def __init__(self):
        ## ignore make error 
        self.ignoreErrors = None
        ## options for the make tool
        self.makeOptions = None
        ## define the basename of the .sln file in case cmake.useIDE = True
        self.slnBaseName = None

## options for the install action 
class OptionsInstall:
    def __init__(self):
        ## use either make tool for installing or 
        # run cmake directly for installing 
        self.useMakeToolForInstall = True
        ## subdir based on installDir() used as install destination directory
        self.installPath = None
        ## add DESTDIR=xxx support for autotools build system
        self.useDestDir = False

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
        
class OptionsCMake:
    def __init__(self): 
        ## use IDE for msvc2008 projects
        self.useIDE = False
        ## use IDE for configuring msvc2008 projects, open IDE in make action instead of running command line orientated make
        self.openIDE = False
        ## use CTest instead of the make utility
        self.useCTest = False
        
## main option class
class Options:
    def __init__(self):
        ## options of the fetch action
        self.unpack = OptionsFetch()
        ## options of the unpack action
        self.unpack = OptionsUnpack()
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
        ## options of the cmake buildSystem
        self.cmake = OptionsCMake()
        
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
        ## use short pathes (usefull for mingw to 
		#  avoid exceeding the maximum path length)
        self.useShortPathes = False

        
    def readFromEnv(self):
        opts = os.getenv( "EMERGE_OPTIONS" )
        if opts == None:
            return False
        opts = opts.split()
        for entry in opts:
            if entry.find('=') == -1:
                utils.debug('incomplete option %s' % entry)
                continue
            (option,value) = entry.split('=')
            print option + " " + value
            if option == "cmake.useIDE":
                # @todo using value from above does not work in case of value=0
                self.cmake.useIDE = True
            elif option == "cmake.openIDE":
                self.cmake.openIDE = True
            elif option == "package.version":
                self.package.version = value
            elif hasattr(self,option):
                # @todo convert "property string" into  cmake.useIDE
                setattr(self,option,value)
            else:
                utils.die("unknown property %s" % option)
