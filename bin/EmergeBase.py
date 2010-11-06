# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import info;
import utils;
import portage;
import os;
import sys;
import datetime;
import emergePlatform;
from ctypes import *

## @todo complete a release and binary merge dir below rootdir 
# 1.  enable build type related merge install settings
# 2a. use different install databases for debug and release
# 3. binary packages which are build type independent should be 
# marked in both databases or should have a separate install database
# question: How to detect reliable this case ? 


ROOTDIR=os.getenv( "KDEROOT" )
COMPILER=os.getenv( "KDECOMPILER" )
DOWNLOADDIR=os.getenv( "DOWNLOADDIR" )
if ( DOWNLOADDIR == None ):
    DOWNLOADDIR=os.path.join( ROOTDIR, "distfiles" )

KDESVNDIR=os.getenv( "KDESVNDIR" )
if ( KDESVNDIR == None ):
    KDESVNDIR=os.path.join( DOWNLOADDIR, "svn-src", "kde" )
KDESVNSERVER=os.getenv( "KDESVNSERVER" )
if ( KDESVNSERVER == None ):
    KDESVNSERVER="svn://anonsvn.kde.org"
KDESVNUSERNAME=os.getenv( "KDESVNUSERNAME" )
KDESVNPASSWORD=os.getenv( "KDESVNPASSWORD" )

# ok, we have the following dirs:
# ROOTDIR: the root where all this is below
# DOWNLOADDIR: the dir under rootdir, where the downloaded files are put into
# WORKDIR: the directory, under which the files are unpacked and compiled.
#            here rootdir/tmp/packagename/work
# IMAGEDIR: the directory, under which the compiled files are installed.
#            here rootdir/tmp/packagename/image

def envAsBool(key):
    """ return value of environment variable as bool value """
    return os.getenv( key ) == "True" or os.getenv( key ) == "1"

class EmergeBase():
    """base class for emerge system - holds attributes and methods required by base classes"""
    
    def __init__( self, className=None, **args):
        utils.debug( "EmergeBase.__init__ called", 2 )

        # if class name has been provided add implicit build time dependency 
        if className and os.getenv('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            packageName = 'internal/%s' % className
            if not packageName in self.subinfo.hardDependencies:
                self.subinfo.hardDependencies[packageName] = 'default'

        if hasattr(self,'alreadyCalled'):
            return
        self.alreadyCalled = True
        self.buildTarget = None

        if "args" in args.keys() and "env" in args["args"].keys():
            env = args["args"]["env"]
        else:
            env = dict( os.environ )

        if "args" in args.keys() and "argv0" in args["args"].keys():
            self.argv0 = args["args"]["argv0"]
        else:
            self.argv0 = sys.argv[ 0 ]

        self.versioned              = False
        self.CustomDefines       = ""
        self.createCombinedPackage  = False
     
        ## specifies if a build type related root directory should be used
        self.useBuildTypeRelatedMergeRoot = False
        if envAsBool("EMERGE_MERGE_ROOT_WITH_BUILD_TYPE"):
            self.useBuildTypeRelatedMergeRoot = True
        
        self.isoDateToday           = str( datetime.date.today() ).replace('-', '')
        
        self.noFetch = False
        if envAsBool( "EMERGE_OFFLINE" ):
            self.noFetch = True
        
        self.noCopy = False
        if envAsBool( "EMERGE_NOCOPY" ):
            self.noCopy = True

        self.noFast = True
        if envAsBool( "EMERGE_NOFAST" ):
            self.noFast = False

        self.noClean = False
        if envAsBool( "EMERGE_NOCLEAN" ) :
            self.noClean = True

        self.forced = False
        if envAsBool( "EMERGE_FORCED" ):
            self.forced = True
            
        self.buildTests = False
        if envAsBool( "EMERGE_BUILDTESTS" ):
            self.buildTests = True

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
        if hasattr(self, "subinfo"):
            self.setup()

    def __adjustPath(self, dir):
        """return adjusted path"""
        if not self.subinfo.options.useShortPathes: 
            return dir
        path = c_char_p(dir)
        len = windll.kernel32.GetShortPathNameA(path, 0, 0)
        if len == 0:
            return dir
        buffer = create_string_buffer('\000' * (len + 1))
        len1 = windll.kernel32.GetShortPathNameA(path, byref(buffer), len+1)
        if utils.verbose() > 0:
	        print "converting " + dir + " to " + buffer.value
        return buffer.value
    
    def abstract():
        import inspect
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')

    def buildType(self):
        """return currently selected build type"""
        Type=os.getenv( "EMERGE_BUILDTYPE" )
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
        """return base directory name for package related work dir"""
        dir = ""
        if self.subinfo.options.useCompilerType == True:
            dir += "%s-" % COMPILER
        if self.isTargetBuild():
            dir += "%s-" % self.buildPlatform()
        if self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE:
            dir += "ide-"
        if self.subinfo.options.useBuildType == False:
            dir += "%s" % (self.buildTarget)
        elif( self.buildType() == None ):
            dir += "%s-%s" % ("default", self.buildTarget)
        else:
            dir += "%s-%s" % (self.buildType(), self.buildTarget)
        return dir

    def imageDirPattern(self):
        """return base directory name for package related image dir"""
        dir = "image"

        # we assume that binary packages are for all compiler and targets
        ## \todo add image dir support for using binary packages for a specific compiler and build type
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            return dir
        
        if self.subinfo.options.useCompilerType == True:
            dir += '-' + COMPILER
        if self.isTargetBuild():
            dir += "-%s" % self.buildPlatform()
        if self.subinfo.options.useBuildType == True:
            dir += '-' + self.buildType()
        dir += '-' + self.buildTarget
        return dir

    def downloadDir(self): 
        """ location of directory where fetched files are  stored """
        return self.__adjustPath(DOWNLOADDIR)
        
    def packageDir(self): 
        """ add documentation """
        return self.__adjustPath(os.path.join( portage.rootDirForPackage( self.category, self.package ), self.category, self.package ))
    
    def filesDir(self):
        """ add documentation """
        return self.__adjustPath(os.path.join( self.packageDir(), "files" ))
        
    def buildRoot(self):
        """return absolute path to the root directory of the currently active package"""
        buildroot    = os.path.join( ROOTDIR, "build", self.category, self.PV )
        return self.__adjustPath(buildroot)

    def workDir(self):
        """return absolute path to the 'work' subdirectory of the currently active package"""
        _workDir = os.path.join( self.buildRoot(), "work" )
        return self.__adjustPath(_workDir)

    def buildDir(self):        
        utils.debug("EmergeBase.buildDir() called" ,2)
        self.setBuildTarget()
        builddir = os.path.join(self.workDir(), self.workDirPattern())
        utils.debug("package builddir is: %s" % builddir,2)
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
            dir = os.path.join( self.imageDir(), self.subinfo.mergeSourcePath() )
        elif not self.subinfo.options.merge.sourcePath == None:
            dir = os.path.join( self.imageDir(), self.subinfo.options.merge.sourcePath )
        else:
            dir = self.imageDir()
        return self.__adjustPath(dir)
                        
    def mergeDestinationDir(self):
        """return absolute path to the merge destination directory of the currently active package. 
        This path may point to a subdir of rootdir in case @ref info.targetMergePath for a specific 
        build target or @ref self.subinfo.options.merge.destinationPath is used 
        """            

        if self.subinfo.hasMergePath():
            dir = os.path.join( ROOTDIR, self.subinfo.mergePath() )
        elif self.isTargetBuild():
            dir = os.path.join(ROOTDIR, self.buildPlatform())
        elif not self.subinfo.options.merge.destinationPath == None:
            dir = os.path.join( ROOTDIR, self.subinfo.options.merge.destinationPath )
        elif not self.useBuildTypeRelatedMergeRoot or self.subinfo.options.merge.ignoreBuildType:
            dir = ROOTDIR
        elif self.buildType() == 'Debug':
            dir = os.path.join(ROOTDIR,'debug')
        elif self.buildType() == 'Release':
            dir = os.path.join(ROOTDIR,'release')
        elif self.buildType() == 'RelWithDebInfo':
            dir = os.path.join(ROOTDIR,'relwithdebinfo')
        else:
            dir = ROOTDIR
        return self.__adjustPath(dir)

    def setBuildTarget( self, target = None):
        utils.debug( "EmergeBase.setBuildTarget called", 2 )
    
        self.subinfo.setBuildTarget(target)
        ## \todo replace self.buildTarget by self.buildTarget()
        self.buildTarget = self.subinfo.buildTarget
        if hasattr(self,'source'):
            self.source.buildTarget = self.subinfo.buildTarget
        
    def setup( self, fileName=None, category=None, package=None, version=None, buildTarget=None):
        if fileName == None:
            ( self.PV, ext ) = os.path.splitext( os.path.basename( self.argv0 ) )
            ( self.category, self.package, self.version ) = portage.getCategoryPackageVersion( self.argv0 )
        else:
            self.category = category
            self.package = package
            self.version = version
            ( self.PV, ext ) = os.path.splitext( os.path.basename( fileName) )
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
            
    def enterImageDir(self):
        if ( not os.path.exists( self.imageDir() ) ):
            return False
        utils.warning("entering the image directory!")
        os.chdir( self.imageDir() )
        if utils.verbose() > 0:
            print "entering: %s" % self.imageDir()
        
        
    def system( self, command, errorMessage="", debuglevel=1, *args, **kw):
        """convencience function for running system commands. 
        This method prints a debug message and then runs a system command. 
        If the system command returns with errors the methos prints an error 
        message and exits if @ref self.subinfo.options.exitOnErrors  is true"""
        
        utils.debug( str(command), debuglevel )
        if utils.system( command, *args, **kw):
            return True
        if self.subinfo.options.exitOnErrors:
            utils.die( "while running %s cmd: %s" % (errorMessage , str(command)) )
        else:
            utils.error( "while running %s cmd: %s" % (errorMessage , str(command)) )
        return False

    def proxySettings(self):
        host = os.getenv('EMERGE_PROXY_HOST')
        port = os.getenv('EMERGE_PROXY_PORT')
        username = os.getenv('EMERGE_PROXY_USERNAME')
        password = os.getenv('EMERGE_PROXY_PASSWORD')
        return [host, port, username, password]
    
        
