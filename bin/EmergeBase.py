# -*- coding: utf-8 -*-

import info;
import utils;
import os;
import sys;
import datetime;

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

EMERGE_MAKE_PROGRAM=os.getenv( "EMERGE_MAKE_PROGRAM" )

# ok, we have the following dirs:
# ROOTDIR: the root where all this is below
# DOWNLOADDIR: the dir under rootdir, where the downloaded files are put into
# WORKDIR: the directory, under which the files are unpacked and compiled.
#            here rootdir/tmp/packagename/work
# IMAGEDIR: the directory, under which the compiled files are installed.
#            here rootdir/tmp/packagename/image


class EmergeBase():
    """base class for emerge system - holds attributes and methods required by base classes"""
    
    def __init__( self, SRC_URI="", **args ):
        if "args" in args.keys() and "env" in args["args"].keys():
            env = args["args"]["env"]
        else:
            env = dict( os.environ )
            
        if "args" in args.keys() and "argv0" in args["args"].keys():
            self.argv0 = args["args"]["argv0"]
        else:
            self.argv0 = sys.argv[ 0 ]
            
        self.SRC_URI                = SRC_URI
        self.noCopy                 = False
        self.noClean                = False
        self.noFast                 = True
        self.buildTests             = False
        self.forced                 = False
        self.versioned              = False
        self.noFetch                = False
        self.CustomDefines       = ""
        self.createCombinedPackage  = False

        self.isoDateToday           = str( datetime.date.today() ).replace('-', '')

        self.setDirectoriesBase()
        #self.msys = msys_build.msys_interface()
        #self.kde  = KDE4BuildSystem()
        
        if os.getenv( "EMERGE_OFFLINE" ) == "True":
            self.noFetch = True
        if os.getenv( "EMERGE_NOCOPY" ) == "True":
            self.noCopy = True
        if os.getenv( "EMERGE_NOFAST" ) == "False":
            self.noFast = False
        if os.getenv( "EMERGE_NOCLEAN" )    == "True":
            self.noClean     = True
        if os.getenv( "EMERGE_FORCED" ) == "True":
            self.forced = True
        if os.getenv( "EMERGE_BUILDTESTS" ) == "True":
            self.buildTests = True

        if COMPILER == "msvc2005":
            self.__compiler = "msvc2005"
        elif COMPILER == "msvc2008":
            self.__compiler = "msvc2008"
        elif COMPILER == "mingw":
            self.__compiler = "mingw"
        else:
            print >> sys.stderr, "emerge error: KDECOMPILER: %s not understood" % COMPILER
            exit( 1 )

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
        utils.debug( "BuildType: %s" % buildType, 2 )
        return buildType

    def compiler(self):
        """return currently selected compiler"""
        return self.__compiler

    def packageDir(): 
        """ add documentation """
        return os.path.join( ROOTDIR, "emerge", "portage", self.category, self.package )
    
    def filesDir():
        """ add documentation """
        return os.path.join( self.packageDir(), "files" )
        
    def workRoot(self):
        """return absolute path to the root directory of the currently active package"""
        workroot    = os.path.join( ROOTDIR, "tmp", self.PV )
        return workroot

    def workDir(self):
        """return absolute path to the 'work' subdirectory of the currently active package"""
        _workDir = os.path.join( self.workRoot(), "work" )
        return _workDir

    def buildDir(self):        
        if( self.buildType() == None ):
            tmp = "%s-%s" % (COMPILER, "default")
        else:
            tmp = "%s-%s" % (COMPILER, self.buildType())
        
        ## \todo for what is this good ?
        #if( not self.buildNameExt == None ):
        #    tmp = "%s-%s" % (COMPILER, self.buildNameExt)

        builddir = os.path.join( self.workDir(), tmp )
        if utils.verbose() > 0:
            print "package builddir is: %s" % builddir
        return builddir

    def imageDir(self):
        """return absolute path to the install root directory of the currently active package
        """
        imagedir = os.path.join( self.workRoot(), "image-" + COMPILER + '-' + self.buildType())
        return imagedir

    def installDir(self):
        """return absolute path to the install directory of the currently active package. 
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath is used 
        """
        if self.subinfo.hasInstallPath():
            installDir = os.path.join( self.imageDir(), self.subinfo.installPath())
        else:
            installDir = self.imageDir()
        return installDir

    def mergeSourceDir(self):
        """return absolute path to the merge source directory of the currently active package. 
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath is used 
        """
        if self.subinfo.hasMergeSourcePath():
            installDir = os.path.join( self.imageDir(), self.subinfo.mergeSourcePath())
        else:
            installDir = self.imageDir()
        return installDir
                        
    def mergeDestinationDir(self):
        """return absolute path to the merge directory of the currently active package. 
        This path may point to a subdir of rootdir in case @ref info.targetMergePath is used 
        """
        if self.subinfo.hasMergePath():
            mergeDir = os.path.join( ROOTDIR, self.subinfo.mergePath())
        else:
            mergeDir = ROOTDIR
        return mergeDir

    def execute( self, cmd=None ):
        """called to run the derived class"""
        """this will be executed from the package if the package is started on its own"""
        """it shouldn't be called if the package is imported as a python module"""

        utils.debug( "EmergeBase.execute called. args: %s" % sys.argv )

        if not cmd:
            command = sys.argv[ 1 ]
            options = ""
            if ( len( sys.argv )  > 2 ):
                options = sys.argv[ 2: ]
        else:
            command = cmd
            options = ""

        self.setDirectoriesBase()

        utils.debug( "command: %s" % command )

        self.subinfo.setBuildTarget()
        self.buildTarget = self.subinfo.buildTarget
        
        # required by some packages
		## \todo  migrate to new style 
        if self.subinfo.hasTargetSourcePath():
            self.instsrcdir = self.subinfo.targetSourcePath()

        self.setDirectories()

        ok = True
        if command   == "fetch":       ok = self.fetch()
        elif command == "cleanimage":  ok = self.cleanup()
        elif command == "unpack":      ok = self.unpack()
        elif command == "compile":     ok = self.compile()
        elif command == "configure":   ok = self.configure()
        elif command == "make":        ok = self.make()
        elif command == "install":     ok = self.install()
        elif command == "test":        ok = self.unittest()
        elif command == "qmerge":      ok = self.qmerge()
        elif command == "unmerge":     ok = self.unmerge()
        elif command == "manifest":    ok = self.manifest()
        elif command == "package":     ok = self.make_package()
        else:
            ok = utils.error( "command %s not understood" % command )

        if ( not ok ):
            utils.die( "command %s failed" % command )

    def setDirectoriesBase( self ):
        """setting all important stuff that isn't coped with in the c'tor"""
        """parts will probably go to infoclass"""
        utils.debug( "setdirectories called", 1 )

        ( self.PV, ext ) = os.path.splitext( os.path.basename( self.argv0 ) )

        ( self.category, self.package, self.version ) = \
                       utils.getCategoryPackageVersion( self.argv0 )

        utils.debug( "setdir category: %s, package: %s" % ( self.category, self.package ) )

        self.cmakeInstallPrefix = ROOTDIR.replace( "\\", "/" )
        utils.debug( "cmakeInstallPrefix: " + self.cmakeInstallPrefix )

        if COMPILER == "msvc2005" or COMPILER == "msvc2008":
            self.cmakeMakefileGenerator = "NMake Makefiles"
            self.cmakeMakeProgramm = "nmake"
        elif COMPILER == "mingw":
            self.cmakeMakefileGenerator = "MinGW Makefiles"
            self.cmakeMakeProgramm = "mingw32-make"
        else:
            utils.die( "KDECOMPILER: %s not understood" % COMPILER )

        if EMERGE_MAKE_PROGRAM:
            self.cmakeMakeProgramm = EMERGE_MAKE_PROGRAM
            utils.debug( "set custom make program: %s" % EMERGE_MAKE_PROGRAM, 1 )

        self.rootdir     = ROOTDIR
                
        # deprecated
        self.kdesvndir = KDESVNDIR
        self.kdesvnserver = KDESVNSERVER
        self.kdesvnuser = KDESVNUSERNAME
        self.kdesvnpass = KDESVNPASSWORD
               
        self.strigidir = os.getenv( "STRIGI_HOME" )
        self.dbusdir = os.getenv( "DBUSDIR" )

    def enterBuildDir(self):
        if ( not os.path.exists( self.workRoot()) ):
            os.mkdir( self.workRoot() )
            if utils.verbose() > 0:
                print "creating: %s" % self.workRoot()
        
        if ( not os.path.exists( self.workDir()) ):
            os.mkdir( self.workDir() )
            if utils.verbose() > 0:
                print "creating: %s" % self.workDir()
        
        if ( not os.path.exists( self.buildDir()) ):
            os.mkdir( self.buildDir() )
            if utils.verbose() > 0:
                print "creating: %s" % self.buildDir()

        os.chdir( self.buildDir() )
        if utils.verbose() > 0:
            print "entering: %s" % self.buildDir()

