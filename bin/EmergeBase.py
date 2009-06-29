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
        self.instsrcdir             = ""
        self.instdestdir            = ""
        self.noCopy                 = False
        self.noClean                = False
        self.noFast                 = True
        self.buildTests             = False
        self.forced                 = False
        self.versioned              = False
        self.noFetch                = False
        self.kdeCustomDefines       = ""
        self.createCombinedPackage  = False

        self.subinfo                = info.infoclass()
        self.buildTarget            = self.subinfo.defaultTarget
        self.Targets                = self.subinfo.svnTargets

        self.isoDateToday           = str( datetime.date.today() ).replace('-', '')

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

        # Build type for kdeCompile() / kdeInstall() - packages
        # "" -> debug and release
        Type=os.getenv( "EMERGE_BUILDTYPE" )
        if ( not Type == None ):
            utils.debug( "BuildType: %s" % Type, 1 )
            self.buildType = Type
        else:
            self.buildType = None

        self.setDirectoriesBase()
        
        if COMPILER == "msvc2005":
            self.compiler = "msvc2005"
        elif COMPILER == "msvc2008":
            self.compiler = "msvc2008"
        elif COMPILER == "mingw":
            self.compiler = "mingw"
        else:
            print >> sys.stderr, "emerge error: KDECOMPILER: %s not understood" % COMPILER
            exit( 1 )

    def abstract():
        import inspect
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')

    def execute( self, cmd=None ):
        """called to run the derived class"""
        """this will be executed from the package if the package is started on its own"""
        """it shouldn't be called if the package is imported as a python module"""
        print self.__class__.__name__
        utils.debug( "base exec called. args: %s" % sys.argv )

        if not cmd:
            command = sys.argv[ 1 ]
            options = ""
            if ( len( sys.argv )  > 2 ):
                options = sys.argv[ 2: ]
        else:
            command = cmd
            options = ""

        utils.debug( "command: %s" % command )

        self.Targets.update( self.subinfo.svnTargets )
        self.Targets.update( self.subinfo.targets )

        self.subinfo.buildTarget = self.subinfo.defaultTarget
        self.buildTarget = self.subinfo.defaultTarget

        if os.getenv( "EMERGE_TARGET" ) in self.Targets.keys():
            self.subinfo.buildTarget = os.getenv( "EMERGE_TARGET" )
            self.buildTarget = os.getenv( "EMERGE_TARGET" )
            
        if self.subinfo.buildTarget in self.subinfo.targets.keys() and self.subinfo.buildTarget in self.subinfo.targetInstSrc.keys():
            self.instsrcdir = self.subinfo.targetInstSrc[ self.subinfo.buildTarget ]

        #self.msys.setDirectories( self.rootdir, self.imagedir, self.workdir, self.instsrcdir, self.instdestdir )
        #self.kde.setDirectories( self.rootdir, self.imagedir, self.workdir, self.instsrcdir, self.instdestdir, self.subinfo )
        
        if self.subinfo.buildTarget in self.subinfo.targets.keys() and not self.kdeSvnPath():
            filenames = []
            for uri in self.subinfo.targets[ self.subinfo.buildTarget ].split():
                filenames.append( os.path.basename( uri ) )
            self.filenames = filenames

        ok = True
        if command   == "fetch":       ok = self.fetch()
        elif command == "cleanimage":       self.cleanup()
        elif command == "unpack":      ok = self.unpack()
        elif command == "compile":     ok = self.compile()
        elif command == "configure":   ok = self.configure()
        elif command == "make":        ok = self.make()
        elif command == "install":     ok = self.install()
        elif command == "test":      ok = self.unittest()
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
        self.downloaddir = DOWNLOADDIR
        self.workdir     = os.path.join( ROOTDIR, "tmp", self.PV, "work" )
        self.imagedir    = os.path.join( ROOTDIR, "tmp", self.PV, "image-" + COMPILER )

        self.packagedir = os.path.join( ROOTDIR, "emerge", "portage", self.category, self.package )
        self.filesdir = os.path.join( self.packagedir, "files" )
        self.kdesvndir = KDESVNDIR
        self.kdesvnserver = KDESVNSERVER
        self.kdesvnuser = KDESVNUSERNAME
        self.kdesvnpass = KDESVNPASSWORD
        self.svndir = os.path.join( self.downloaddir, "svn-src", self.package )
       
        self.strigidir = os.getenv( "STRIGI_HOME" )
        self.dbusdir = os.getenv( "DBUSDIR" )
