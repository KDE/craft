#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import utils
import portage
import os
import sys
import datetime
import emergePlatform
from ctypes import *

## @todo complete a release and binary merge dir below rootdir
# 1.  enable build type related otDmerge install settings
# 2a. use different install databases for debug and release
# 3. binary packages which are build type independent should be
# marked in both databases or should have a separate install database
# question: How to detect reliable this case ?


ROOTDIR = os.getenv( "KDEROOT" )
COMPILER = os.getenv( "KDECOMPILER" )
DOWNLOADDIR = os.getenv( "DOWNLOADDIR" )
if ( DOWNLOADDIR == None ):
    DOWNLOADDIR = os.path.join( ROOTDIR, "distfiles" )

KDESVNDIR = os.getenv( "KDESVNDIR" )
if ( KDESVNDIR == None ):
    KDESVNDIR = os.path.join( DOWNLOADDIR, "svn-src", "kde" )
KDESVNSERVER = os.getenv( "KDESVNSERVER" )
if ( KDESVNSERVER == None ):
    KDESVNSERVER = "svn://anonsvn.kde.org"
KDESVNUSERNAME = os.getenv( "KDESVNUSERNAME" )
KDESVNPASSWORD = os.getenv( "KDESVNPASSWORD" )

# ok, we have the following dirs:
# ROOTDIR: the root where all this is below
# DOWNLOADDIR: the dir under rootdir, where the downloaded files are put into
# WORKDIR: the directory, under which the files are unpacked and compiled.
#            here rootdir/tmp/packagename/work
# IMAGEDIR: the directory, under which the compiled files are installed.
#            here rootdir/tmp/packagename/image


class EmergeBase(object):
    """base class for emerge system - holds attributes and methods required by base classes"""

    def __init__( self, className=None, **args):
        """args really should be documented, see self.argv0 below"""
        # TODO: some __init__  of subclasses need to already have been
        # called here. That is really the wrong way round.
        object.__init__(self)
        utils.debug( "EmergeBase.__init__ called", 2 )

        if not hasattr(self, 'subinfo'):
            # see the TODO above. This helps pylint understand the code, otherwise
            # it generates tons of error messages.
            self.subinfo = None
        if not hasattr(self, 'buildSystemType'):
            self.buildSystemType = None

        # if class name has been provided add implicit build time dependency
        if className and utils.envAsBool('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            packageName = 'internal/%s' % className
            if not packageName in self.subinfo.buildDependencies:
                self.subinfo.buildDependencies[packageName] = 'default'

        if hasattr(self,'alreadyCalled'):
            return
        self.alreadyCalled = True
        self.buildTarget = None

        if "args" in args.keys() and "argv0" in args["args"].keys():
            self.argv0 = args["args"]["argv0"]
        else:
            self.argv0 = sys.argv[ 0 ]

        self.versioned              = False
        self.CustomDefines       = ""
        self.createCombinedPackage  = False

        ## specifies if a build type related root directory should be used
        self.useBuildTypeRelatedMergeRoot = False
        if utils.envAsBool("EMERGE_MERGE_ROOT_WITH_BUILD_TYPE"):
            self.useBuildTypeRelatedMergeRoot = True

        self.isoDateToday           = str( datetime.date.today() ).replace('-', '')

        self.noFetch = utils.envAsBool( "EMERGE_OFFLINE" )
        self.noCopy = utils.envAsBool( "EMERGE_NOCOPY")
        self.noFast = utils.envAsBool( "EMERGE_NOFAST", default=True )
        self.noClean = utils.envAsBool( "EMERGE_NOCLEAN" )
        self.forced = utils.envAsBool( "EMERGE_FORCED" )
        self.buildTests = utils.envAsBool( "EMERGE_BUILDTESTS" )

        if COMPILER == "msvc2005":
            self.__compiler = "msvc2005"
        elif COMPILER == "msvc2008":
            self.__compiler = "msvc2008"
        elif COMPILER == "msvc2010":
            self.__compiler = "msvc2010"
        elif COMPILER == "mingw":
            self.__compiler = "mingw"
        elif COMPILER == "mingw4":
            self.__compiler = "mingw4"
        else:
            print >> sys.stderr, "emerge error: KDECOMPILER: '%s' not understood" % COMPILER
            exit( 1 )
        self.rootdir = ROOTDIR
        if self.subinfo:
            self.setup()

    def __adjustPath(self, directory):
        """return adjusted path"""
        if not self.subinfo.options.useShortPathes:
            return directory
        path = c_char_p(directory)
        length = windll.kernel32.GetShortPathNameA(path, 0, 0)
        if length == 0:
            return directory
        buf = create_string_buffer('\000' * (length + 1))
        windll.kernel32.GetShortPathNameA(path, byref(buf), length+1) # ignore function result...
        if utils.verbose() > 0:
            print "converting " + directory + " to " + buf.value
        return buf.value

    def buildType(self):
        """return currently selected build type"""
        Type = os.getenv( "EMERGE_BUILDTYPE" )
        if ( not Type == None ):
            buildType = Type
        else:
            buildType = None
        return buildType

    def compiler(self):
        """return currently selected compiler"""
        return self.__compiler

    def isTargetBuild(self):
        if not emergePlatform.isCrossCompilingEnabled():
            return False
        else:
            return os.getenv( "EMERGE_BUILD_STEP" ) == "target"

    def isHostBuild(self):
        if not emergePlatform.isCrossCompilingEnabled():
            return True
        else:
            return os.getenv( "EMERGE_BUILD_STEP" ) == "host"

    def buildPlatform(self):
        """return the cross-compiling target platform"""
        if self.isTargetBuild():
            return os.getenv( "EMERGE_TARGET_PLATFORM" )
        else:
            return "WIN32"

    def buildArchitecture(self):
        """return the target CPU architecture"""
        if self.isTargetBuild():
            return os.getenv( "EMERGE_TARGET_ARCHITECTURE" )
        else:
            return os.getenv( "EMERGE_ARCHITECTURE" )

    def workDirPattern(self):
        """return base directory name for package related work directory"""
        directory = ""
        if self.subinfo.options.useCompilerType == True:
            directory += "%s-" % COMPILER
        if self.isTargetBuild():
            directory += "%s-" % self.buildPlatform()
        if self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE:
            directory += "ide-"
        if self.subinfo.options.useBuildType == False:
            directory += "%s" % (self.buildTarget)
        elif( self.buildType() == None ):
            directory += "%s-%s" % ("default", self.buildTarget)
        else:
            directory += "%s-%s" % (self.buildType(), self.buildTarget)
        return directory

    def imageDirPattern(self):
        """return base directory name for package related image directory"""
        directory = "image"

        # we assume that binary packages are for all compiler and targets
        ## \todo add image directory support for using binary packages for a specific compiler and build type
        if self.buildSystemType == 'binary':
            return directory

        if self.subinfo.options.useCompilerType == True:
            directory += '-' + COMPILER
        if self.isTargetBuild():
            directory += "-%s" % self.buildPlatform()
        if self.subinfo.options.useBuildType == True:
            directory += '-' + self.buildType()
        directory += '-' + self.buildTarget
        return directory

    def downloadDir(self):
        """ location of directory where fetched files are  stored """
        return self.__adjustPath(DOWNLOADDIR)

    def sourceDir(self):
        utils.abstract()

    def packageDir(self):
        """ add documentation """
        return self.__adjustPath(os.path.join( portage.rootDirForPackage( self.category, self.package ), self.category, self.package ))

    def buildRoot(self):
        """return absolute path to the root directory of the currently active package"""
        buildroot    = os.path.join( ROOTDIR, "build", self.category, self.PV )
        return self.__adjustPath(buildroot)

    def workDir(self):
        """return absolute path to the 'work' subdirectory of the currently active package"""
        _workDir = os.path.join( self.buildRoot(), "work" )
        return self.__adjustPath(_workDir)

    def buildDir(self):
        utils.debug("EmergeBase.buildDir() called", 2)
        self.setBuildTarget()
        builddir = os.path.join(self.workDir(), self.workDirPattern())
        if self.subinfo.options.unpack.unpackIntoBuildDir and self.subinfo.hasTargetSourcePath():
            builddir = os.path.join(builddir, self.subinfo.targetSourcePath())
        utils.debug("package builddir is: %s" % builddir, 2)
        return self.__adjustPath(builddir)

    def imageDir(self):
        """return absolute path to the install root directory of the currently active package
        """
        imageDir =  os.path.join( self.buildRoot(), self.imageDirPattern() )
        return self.__adjustPath(imageDir)

    def installDir(self):
        """return absolute path to the install directory of the currently active package.
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath is used
        """
        if self.subinfo.hasInstallPath():
            installDir = os.path.join( self.imageDir(), self.subinfo.installPath())
        elif self.subinfo.options.install.installPath:
            installDir = os.path.join(self.imageDir(), self.subinfo.options.install.installPath)
        else:
            installDir = self.imageDir()
        return self.__adjustPath(installDir)

    def mergeSourceDir(self):
        """return absolute path to the merge source directory of the currently active package.
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath for a
        specific target or @ref self.subinfo.options.merge.sourcePath is used
        """
        if self.subinfo.hasMergeSourcePath():
            directory = os.path.join( self.imageDir(), self.subinfo.mergeSourcePath() )
        elif not self.subinfo.options.merge.sourcePath == None:
            directory = os.path.join( self.imageDir(), self.subinfo.options.merge.sourcePath )
        else:
            directory = self.imageDir()
        return self.__adjustPath(directory)

    def mergeDestinationDir(self):
        """return absolute path to the merge destination directory of the currently active package.
        This path may point to a subdir of rootdir in case @ref info.targetMergePath for a specific
        build target or @ref self.subinfo.options.merge.destinationPath is used
        """

        if self.subinfo.hasMergePath():
            directory = os.path.join( ROOTDIR, self.subinfo.mergePath() )
        elif self.isTargetBuild():
            directory = os.path.join(ROOTDIR, self.buildPlatform())
        elif not self.subinfo.options.merge.destinationPath == None:
            directory = os.path.join( ROOTDIR, self.subinfo.options.merge.destinationPath )
        elif not self.useBuildTypeRelatedMergeRoot or self.subinfo.options.merge.ignoreBuildType:
            directory = ROOTDIR
        elif self.buildType() == 'Debug':
            directory = os.path.join(ROOTDIR,'debug')
        elif self.buildType() == 'Release':
            directory = os.path.join(ROOTDIR,'release')
        elif self.buildType() == 'RelWithDebInfo':
            directory = os.path.join(ROOTDIR,'relwithdebinfo')
        else:
            directory = ROOTDIR
        return self.__adjustPath(directory)

    def packageDestinationDir( self, withBuildType=True ):
        """return absolute path to the directory where binary packages are placed into.
        Default is to optionally append build type subdirectory"""

        utils.debug( "EmergeBase.packageDestinationDir called", 2 )
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )

        if withBuildType:
            if utils.envAsBool( "EMERGE_MERGE_ROOT_WITH_BUILD_TYPE" ):
                dstpath = os.path.join( dstpath, self.buildType())

        if not os.path.exists(dstpath):
            utils.createDir(dstpath)
        return dstpath

    def setBuildTarget( self, target = None):
        utils.debug( "EmergeBase.setBuildTarget called", 2 )

        self.subinfo.setBuildTarget(target)
        ## \todo replace self.buildTarget by self.buildTarget()
        self.buildTarget = self.subinfo.buildTarget
        if hasattr(self,'source'):
            # pylint: disable=E1101
            # this class never defines self.source, that happens only
            # in MultiSource.
            self.source.buildTarget = self.subinfo.buildTarget

    def setup( self, fileName=None, category=None, package=None, version=None, buildTarget=None):
        if fileName == None:
            self.PV, _ = os.path.splitext( os.path.basename( self.argv0 ) )
            self.category, self.package, self.version = portage.getCategoryPackageVersion( self.argv0 )
        else:
            self.category = category
            self.package = package
            self.version = version
            self.PV, _ = os.path.splitext( os.path.basename( fileName) )
        self.setBuildTarget(buildTarget)

    def enterBuildDir(self):
        utils.debug( "EmergeBase.enterBuildDir called", 2 )

        if ( not os.path.exists( self.buildDir() ) ):
            os.makedirs( self.buildDir() )
            if utils.verbose() > 0:
                print "creating: %s" % self.buildDir()

        os.chdir( self.buildDir() )
        if utils.verbose() > 0:
            print "entering: %s" % self.buildDir()

    def enterSourceDir(self):
        if ( not os.path.exists( self.sourceDir() ) ):
            return False
        utils.warning("entering the source directory!")
        os.chdir( self.sourceDir() )
        if utils.verbose() > 0:
            print "entering: %s" % self.sourceDir()

    def system( self, command, errorMessage="", debuglevel=1, *args, **kw):
        """convencience function for running system commands.
        This method prints a debug message and then runs a system command.
        If the system command returns with errors the methos prints an error
        message and exits if @ref self.subinfo.options.exitOnErrors  is true"""

        utils.debug( str(command), debuglevel )
        if utils.system( command, *args, **kw):
            return True
        if self.subinfo.options.exitOnErrors:
            utils.die( "while running %s cmd: %s" % (errorMessage, str(command)) )
        else:
            utils.error( "while running %s cmd: %s" % (errorMessage, str(command)) )
        return False

    def proxySettings(self):
        host = os.getenv('EMERGE_PROXY_HOST')
        port = os.getenv('EMERGE_PROXY_PORT')
        username = os.getenv('EMERGE_PROXY_USERNAME')
        password = os.getenv('EMERGE_PROXY_PASSWORD')
        return [host, port, username, password]

