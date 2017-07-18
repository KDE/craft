## @package property handling
#
# (c) copyright 2009-2011 Ralf Habacker <ralf.habacker@freenet.de>
#
#
# properties from classes in this package could be set
#
# - by package scripts,
# - by setting the 'EMERGE_OPTIONS' environment variable or
# - by command line
#
# for example:
#
# in portage/subdir/package/file.py
#   ...
#   self.subinfo.options.cmake.openIDE=1
#
# or
#
# craft "--options=cmake.openIDE=1" --make kdewin-installer
#
# or
#
# set EMERGE_OPTIONS=cmake.openIDE=1
# craft --make kdewin-installer
#
# The parser in this package is able to set all attributes
#
# for example:
#
#  craft "--options=unpack.unpackIntoBuildDir=1 useBuildType=1" --make <package>
#
import os
import inspect
import shlex

from CraftDebug import craftDebug, deprecated
from CraftConfig import  *
import utils
import portage


class OptionsBase(object):
    def __init__(self):
        pass

class OptionsPortage(OptionsBase):
    def __init__(self):
        self._packages = dict()

    def __setattr__(self, name, value):
        if name == "_packages":
            object.__setattr__(self, name, value)
        else:
            self._packages[name] = value

    def __getattr__(self, name):
        if name in self._packages:
            return self._packages[name]
        else:
            return True


## options for enabling or disabling features of KDE
## in the future, a certain set of features make up a 'profile' together
class OptionsFeatures(OptionsBase):
    def __init__(self):
        class PhononBackend(OptionsBase):
            def __init__(self):
                ## options for the phonon backend
                self.vlc = True
                self.ds9 = False

        self.phononBackend = PhononBackend()

        ## option whether to build nepomuk
        self.nepomuk = True

        ## enable python support in several packages.
        self.pythonSupport = False

        ## stick to the gcc 4.4.7 version
        self.legacyGCC = False

        ## enable or disable the dependency to plasma
        self.fullplasma = False

## options for the fetch action
class OptionsFetch(OptionsBase):
    def __init__(self):
        ## option comment
        self.option = None
        self.ignoreExternals = False
        ## enable submodule support in git single branch mode
        self.checkoutSubmodules = False

## options for the unpack action
class OptionsUnpack(OptionsBase):
    def __init__(self):
        ## By default archives are unpackaged into the workdir.
        #  Use this option to unpack archives into recent build directory
        self.unpackIntoBuildDir = False
        #  Use this option to run 3rd party installers
        self.runInstaller = False

## options for the configure action
class OptionsConfigure(OptionsBase):
    def __init__(self):
        ## with this option additional arguments could be added to the configure commmand line
        self.args = None
        ## with this option additional arguments could be added to the configure commmand line (for static builds)
        self.staticArgs = None
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

        ## run autogen in autotools
        self.bootstrap = False

        # do not use default include path
        self.noDefaultInclude = False

        ## do not use default lib path
        self.noDefaultLib = False

        ## set this attribute in case a non standard configuration
        # tool is required (supported currently by QMakeBuildSystem only)
        self.tool = False

        # do not add --prefix on msys
        self.noDefaultOptions = False

        # cflags currently only used for autotools
        self.cflags = ""

        # cxxflags currently only used for autotools
        self.cxxflags = ""

        # ldflags currently only used for autotools
        self.ldflags = ""

        # the project file, this is either a .pro for qmake or a sln for msbuild
        self.projectFile = None


## options for the make action
class OptionsMake(OptionsBase):
    def __init__(self):
        ## ignore make error
        self.ignoreErrors = None
        ## options for the make tool
        self.makeOptions = None
        ## define the basename of the .sln file in case cmake.useIDE = True
        self.slnBaseName = None
        self.supportsMultijob = True

## options for the install action
class OptionsInstall(OptionsBase):
    def __init__(self):
        ## use either make tool for installing or
        # run cmake directly for installing
        self.useMakeToolForInstall = True
        ## add DESTDIR=xxx support for autotools build system
        self.useDestDir = True

## options for the merge action
class OptionsMerge(OptionsBase):
    def __init__(self):
        ## subdir based on installDir() used as merge source directory
        self.sourcePath = None

## options for the package action
class OptionsPackage(OptionsBase):
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
        ## pack from subdir of imageDir()
        # currently supported by SevenZipPackager
        self.packageFromSubDir = None
        ## use architecture in package name
        # currently supported by SevenZipPackager
        self.withArchitecture = False
        ## add file digests to the package located in the manifest sub dir
        # currently supported by SevenZipPackager
        self.withDigests = True
        ##disable stripping of binary files
        #needed for mysql, striping make the library unusable
        self.disableStriping = False

        ##disable the binary cache for this package
        self.disableBinaryCache = False

class OptionsCMake(OptionsBase):
    def __init__(self):
        ## use IDE for msvc2008 projects
        self.useIDE = False
        ## use IDE for configuring msvc2008 projects, open IDE in make action instead of running command line orientated make
        self.openIDE = False
        ## use CTest instead of the make utility
        self.useCTest = craftSettings.getboolean("General","EMERGE_USECTEST", False )


class OptionsGit(OptionsBase):
    def __init__(self):
        ## enable support for applying patches in 'format-patch' style with 'git am' (experimental support)
        self.enableFormattedPatch = False

## main option class
class Options(object):
    def __init__(self, optionslist=None):
        ## options for the dependency generation
        self.features = OptionsFeatures()
        ## options for package exclusion
        self.packages = OptionsPortage()
        ## options of the fetch action
        self.fetch = OptionsFetch()
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
        ## options of the git module
        self.git = OptionsGit()

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

        ## there is a special option available already
        self.buildTools = False
        self.buildStatic = craftSettings.getboolean("Compile", "Static")


        self.useShadowBuild = True

        #### end of user configurable part
        self.__verbose = False
        self.__errors = False
        self.__readFromList(craftSettings.get( "General", "EMERGE_OPTIONS", "").split(" "))
        self.readFromEnv()
        self.__readFromList(optionslist)

    def readFromEnv( self ):
        """ read craft related variables from environment and map them to public
        attributes in the option class and sub classes """
        _o = os.getenv("EMERGE_OPTIONS")
        if _o:
            _o = _o.split(" ")
        else:
            _o = []
        self.__readFromList(_o)

    def isActive(self, package):
        return not portage.PortageInstance.ignores.match(package)

    def __setInstanceAttribute( self, key, value ):
        """set attribute in an instance"""
        currentObject = self
        currentKey = None
        for currentKey in key.split('.'):
            if currentKey == "options": continue

            if hasattr(currentObject, currentKey):
                o = getattr(currentObject, currentKey)
                if not isinstance(o, OptionsBase):
                    continue
                else:
                    currentObject = o
            else:
                if isinstance(currentObject, OptionsPortage):
                    break
                return False

        # if the type is already bool, we'll keep it that way and interpret the string accordingly
        if type(getattr(currentObject, currentKey)) is bool:
            value = value in ['True', 'true', '1', 'ON', 'on']

        setattr( currentObject, currentKey, value )
        return True



    def __readFromList( self, opts ):
        """collect properties from a list of key=value string"""
        if opts == None:
            return False
        result = False
        for entry in opts:
            if entry.find('=') == -1:
                craftDebug.log.debug('incomplete option %s' % entry)
                continue
            (key, value) = entry.split( '=', 1 )
            if self.__setInstanceAttribute(key, value):
                result = True
                continue
        return result
