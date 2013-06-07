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
# emerge "--options=cmake.openIDE=1" --make kdewin-installer
#
# or
#
# set EMERGE_OPTIONS=cmake.openIDE=1
# emerge --make kdewin-installer
#
# The parser in this package is able to set all attributes
#
# for example:
#
#  emerge "--options=unpack.unpackIntoBuildDir=1 useBuildType=1" --make <package>
#
import os
import utils
import inspect
import shlex

class OptionsBase(object):
    def __init__(self):
        pass

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

        ## options whether to build nepomuk
        self.nepomuk = True

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
        ## subdir based on installDir() used as install destination directory
        self.installPath = None
        ## add DESTDIR=xxx support for autotools build system
        self.useDestDir = True

## options for the merge action
class OptionsMerge(OptionsBase):
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
        
        

class OptionsCMake(OptionsBase):
    def __init__(self):
        ## use IDE for msvc2008 projects
        self.useIDE = False
        ## use IDE for configuring msvc2008 projects, open IDE in make action instead of running command line orientated make
        self.openIDE = False
        ## use CTest instead of the make utility
        self.useCTest = utils.envAsBool("EMERGE_USECTEST")

class OptionsGit(OptionsBase):
    def __init__(self):
        ## enable support for applying patches in 'format-patch' style with 'git am' (experimental support)
        self.enableFormattedPatch = False

## main option class
class Options(object):
    def __init__(self):
        ## options for the dependency generation
        self.features = OptionsFeatures()
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
        ## use short pathes (usefull for mingw to
        #  avoid exceeding the maximum path length)
        self.useShortPathes = False

        ## there is a special option available already
        self.buildTests = utils.envAsBool("EMERGE_BUILDTESTS")
        self.buildTools = "False"
        self.buildStatic = "False"

        #### end of user configurable part
        self.__instances = dict()
        self.__verbose = False
        self.__errors = False

    def readFromEnv( self ):
        """ read emerge related variables from environment and map them to public
        attributes in the option class and sub classes """
        self.__collectAttributes()
        if 'EMERGE_OPTIONS' in os.environ:
            self.__readFromString(os.environ['EMERGE_OPTIONS'])

    def __collectAttributes( self, instance=None, container=None ):
        """ collect all public attributes this class and subclasses
        """
        if instance == None: instance = self
        if container == None: container = self.__instances
        # first save instance object
        container['.'] = [instance, dict()]

        # now check all children
        for key, value in inspect.getmembers(instance):
            if key.startswith('__') or type(value).__name__.startswith('instance'):
                continue
            if inspect.ismethod(value):
                continue
            # we have found a child that in itself could have children again
            if isinstance(value, OptionsBase):
                container[key.lower()] = dict()
                self.__collectAttributes(value, container[key.lower()])
            else:
                # simply append properties here
                container['.'][1][key.lower()] = [key, value]

        if self.__verbose:
            for key in container:
                print(container[key])

    def __setInstanceAttribute( self, key, value ):
        """set attribute in an instance"""
        currentObject = None
        currentKey = None
        currentDict = self.__instances
        for keyparticle in key.split('.'):
            if keyparticle.lower() in currentDict:
                #print("found keyparticle as branch", keyparticle)
                currentDict = currentDict[keyparticle.lower()]
            elif keyparticle.lower() in currentDict['.'][1]:
                #print("found keyparticle as node", keyparticle)
                currentObject = currentDict['.'][0]
                currentKey = currentDict['.'][1][keyparticle.lower()][0]
        if not currentObject or not currentKey:
            return False

        # if the type is already bool, we'll keep it that way and interpret the string accordingly
        if type(getattr(currentObject, currentKey)) is bool:
            value = value in ['True', 'true', '1', 'ON', 'on']

        setattr( currentObject, currentKey, value )

#        p = ""
#        if self.__instances[a][0]:
#            p += self.__instances[a][0] + '.'
#        if self.__verbose:
#            print("mapped %s to %s%s with value %s" % (origKey, p, self.__instances[a][2][b][0], value))
        return True

    def __readFromString( self, opts ):
        """collect properties from a space delimited key=valule string"""
        if opts == None:
            return False
        # keep escapes inside this string - otherwise spaces cannot be given over
        opts = shlex.split(opts, posix=True)
        result = False
        for entry in opts:
            if entry.find('=') == -1:
                utils.debug('incomplete option %s' % entry, 3)
                continue
            (key, value) = entry.split( '=', 1 )
            if self.__setInstanceAttribute(key, value ):
                result = True
                continue
        return result
