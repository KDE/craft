# -*- coding: utf-8 -*-
""" \package BuildSystem"""

from EmergeBase import *
import utils;

class BuildSystemBase(EmergeBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    noClean = False
    debug = True

    def __init__(self,type,configureOptions="", makeOptions=""):
        """constructor"""
        EmergeBase.__init__(self)
        self.buildSystemType = type
        self.configureOptions = configureOptions
        self.makeOptions = makeOptions
                
    ## \todo not sure if buildType and options are used anywhere, if not remove them
    def configure(self, buildType=None): 
        """configure the target"""
        abstract()

    def install(self): 
        """install the target into local install directory"""
        abstract()

    def uninstall(self): 
        """uninstall the target from the local install directory"""
        abstract()

    def runTests(self): 
        """run the test - if available - for the target"""
        abstract()

    def make(self, buildType=None): 
        """make the target by runnning the related make tool"""
        abstract()
            
    ## \todo not sure if buildType and customDefines are used anywhere, if not remove them"""
    def compile(self, buildType=None, customOptions=""):
        """convencience method - runs configure() and make()"""
        if( not self.buildType() == None ) :
            if( not ( self.configure( self.buildType(), customOptions ) and self.make( self.buildType() ) ) ):
                return False
            else:
                if( not ( self.configure( "Debug", customOptions ) and self.make( "Debug" ) ) ):
                    return False
                if( not ( self.configure( "Release", customOptions ) and self.make( "Release" ) ) ):
                    return False
            return True

    def setDirectories(self):
        return
    
    def configureSourceDir(self):
        """returns source dir used for configure step"""
        if hasattr(self,'source'):
            sourcedir = self.source.sourceDir()
        else:
            sourcedir = self.sourceDir()
       
        if self.subinfo.hasConfigurePath():
            sourcedir = os.path.join(sourcedir,self.subinfo.configurePath())
        return sourcedir
        

class BinaryBuildSystem(BuildSystemBase):
    def __init__( self, configureOptions="", makeOptions=""):
        BuildSystemBase.__init__(self,"binary", configureOptions,makeOptions)
        
    def configure( self, buildType=None, customOptions="" ):
        return True

    def make( self, buildType=None ):
        return True

    # nothing to do - unpack hasd done this job already
    def install( self, buildType=None ):
        return True
        
    def runTest( self ):
        return False
   
   
class CMakeBuildSystem(BuildSystemBase):
    """ cmake build support """
    def __init__( self, configureOptions="",makeOptions=""):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self,"cmake",configureOptions,makeOptions)

    def svnPath(self): 
        return ""
                                
    def configureDefaultDefines( self ):
        """returns default configure options"""
        sourcedir = self.configureSourceDir()
        ## \todo should install prefix not be set to mergeDir ?`
        options = "\"%s\" -DCMAKE_INSTALL_PREFIX=\"%s\" " % \
              ( sourcedir, self.rootdir.replace( "\\", "/" ) )

        options = options + "-DCMAKE_INCLUDE_PATH=\"%s\" " % \
                os.path.join( self.rootdir, "include" ).replace( "\\", "/" )

        options = options + "-DCMAKE_LIBRARY_PATH=\"%s\" " % \
                os.path.join( self.rootdir, "lib" ).replace( "\\", "/" )

        if( not self.buildType() == None ):
            options  = options + "-DCMAKE_BUILD_TYPE=%s" % self.buildType()             
                
        return options

    def configure( self, buildType=None, customDefines="" ):
        """Using cmake"""

        if not self.noClean:
            utils.cleanDirectory( self.builddir )
            
        self.enterBuildDir()
        
        defines = self.configureDefaultDefines()
        
        command = r"""cmake -G "%s" %s %s""" % \
              ( self.cmakeMakefileGenerator, \
                defines, \
                self.configureOptions )

        if utils.verbose() > 0:
            print "configuration command: %s" % command
        utils.system( command ) or utils.die( "while CMake'ing. cmd: %s" % command )
        return True

    def make( self, buildType=None ):
        """run the *make program"""

        self.enterBuildDir()
        
        command = self.cmakeMakeProgramm

        if utils.verbose() > 1:
            command += " VERBOSE=1"
        
        command += ' %s' % self.makeOptions

        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def __install( self, buildType=None ):
        """Using *make install"""

        self.enterBuildDir()

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s DESTDIR=%s install%s" % ( self.cmakeMakeProgramm, self.imageDir(), fastString ) ) or utils.die( "while installing. cmd: %s" % "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imageDir() ) )
        return True

    def compile( self, customDefines=""):
        """making all required stuff for compiling cmake based modules"""
        if( not self.buildType() == None ) :
            if( not ( self.configure( self.buildType(), customDefines ) and self.make( self.buildType() ) ) ):
                return False
        else:
            if( not ( self.configure( "Debug", customDefines ) and self.make( "Debug" ) ) ):
                return False
            if( not ( self.configure( "Release", customDefines ) and self.make( "Release" ) ) ):
                return False
        return True

    def install( self ):
        """making all required stuff for installing cmake based modules"""
        if( not self.buildType() == None ):
            if( not self.__install( self.buildType() ) ):
                return False
        else:
            if( not self.__install( "debug" ) ):
                return False
            if( not self.__install( "release" ) ):
                return False
        utils.fixCmakeImageDir( self.imageDir(), self.rootdir )
        return True

    def runTest( self ):
        """running cmake based unittests"""

        self.enterbuildDir()

        if utils.verbose() > 0:
            print "builddir: " + builddir

        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True

        
class QMakeBuildSystem(BuildSystemBase):
    def __init__( self, configureOptions="", makeOptions=""):
        BuildSystemBase.__init__(self,"qmake",configureOptions,makeOptions)
        
    def configure( self, buildType=None, customOptions="" ):
        """Using qmake"""
            
        self.enterBuildDir()
        
        # here follows some automatic configure tool detection
        # 1. search for configure.exe 
        # 2. search for a pro-file named as the package 
        # 3. if a pro-file is available through configureOptions, run it with qmake
        # 4. if a complete configure command line is available run it 
        configTool = os.path.join(self.sourcedir,"configure.exe")
        topLevelProFile = os.path.join(self.sourcedir,self.package + ".pro")
        if os.path.exists(configTool):
            command = configTool + " " + self.configureOptions()
        elif os.path.exists(topLevelProFile):
            command = "qmake " + topLevelProFile
        elif self.configureOptions() != "":
            command = "qmake " + self.configureOptions()
        elif self.configureTool() != "":
            command = self.configureTool()
        else:
            utils.die("could not find configure.exe or top level pro-file, please take a look into the source and setup the config process.")

        if utils.verbose() > 0:
            print "configuration command: %s" % command
        utils.system( command ) or utils.die( "while CMake'ing. cmd: %s" % command )
        return True

    def makeOptions(self):
        return ""

    def make( self, buildType=None ):
        """Using the make program"""

        self.enterBuildDir()

        command = self.cmakeMakeProgramm + " " + self.makeOptions()
        # adding Targets later
        if utils.verbose() > 1:
            command += " VERBOSE=1"
        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def __install( self, buildType=None ):
        """Using *make install"""

        self.enterBuildDir()

        if utils.verbose() > 0:
            print "builddir: " + builddir

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s DESTDIR=%s install%s" % ( self.cmakeMakeProgramm, self.imageDir(), fastString ) ) or utils.die( "while installing. cmd: %s" % "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imageDir() ) )
        return True

    def compile( self, customDefines=""):
        """making all required stuff for compiling cmake based modules"""
        if( not self.buildType() == None ) :
            if( not ( self.configure( self.buildType(), customDefines ) and self.make( self.buildType() ) ) ):
                return False
        else:
            if( not ( self.configure( "Debug", customDefines ) and self.make( "Debug" ) ) ):
                return False
            if( not ( self.configure( "Release", customDefines ) and self.make( "Release" ) ) ):
                return False
        return True

    def install( self ):
        """making all required stuff for installing cmake based modules"""
        if( not self.buildType() == None ):
            if( not self.__install( self.buildType() ) ):
                return False
        else:
            if( not self.__install( "debug" ) ):
                return False
            if( not self.__install( "release" ) ):
                return False
        utils.fixCmakeImageDir( self.imageDir(), self.rootdir )
        return True

    def runTest( self ):
        """running cmake based unittests"""

        self.enterBuildDir()
        
        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True

from Source.SvnSource import *

class KDE4BuildSystem(SvnSource,BuildSystemBase):
    # todo fix setting sourcePath correctly
    sourcePath = ""
    def __init__( self, env = dict( os.environ ) ):
        SvnSource.__init__(self)
        BuildSystemBase.__init__(self,"kde4")
        
        for key in ["KDESVNUSERNAME", "KDESVNPASSWORD", "KDECOMPILER", "KDESVNDIR", "KDESVNSERVER", 
                    "EMERGE_BUILDTYPE", "EMERGE_OFFLINE", "EMERGE_NOCOPY", "EMERGE_NOCLEAN", "EMERGE_NOFAST", "EMERGE_BUILDTESTS", "EMERGE_MAKE_PROGRAM", "DIRECTORY_LAYOUT" ]:
            if not key in env.keys():
                env[ key ] = None
        self.COMPILER            = env[ "KDECOMPILER" ]
        self.KDESVNUSERNAME      = env[ "KDESVNUSERNAME" ]
        self.KDESVNPASSWORD      = env[ "KDESVNPASSWORD" ]
        self.KDESVNDIR           = env[ "KDESVNDIR" ]
        self.KDESVNSERVER        = env[ "KDESVNSERVER" ]
        if ( self.KDESVNDIR    == None ):
            self.KDESVNDIR       = os.path.join( DOWNLOADDIR, "svn-src", "kde" )
        if ( self.KDESVNSERVER == None ):
            self.KDESVNSERVER    = "svn://anonsvn.kde.org"
        self.BUILDTYPE           = env[ "EMERGE_BUILDTYPE" ]
        if ( self.BUILDTYPE not in ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"] ):
            self.BUILDTYPE=None
        self.OFFLINE = env[ "EMERGE_OFFLINE" ]
        self.NOCOPY = env[ "EMERGE_NOCOPY" ]
        self.NOCLEAN = env[ "EMERGE_NOCLEAN" ]
        self.NOFAST = env[ "EMERGE_NOFAST" ]
        self.BUILDTESTS = env[ "EMERGE_BUILDTESTS" ]
        self.DIRECTORY_LAYOUT = env[ "DIRECTORY_LAYOUT" ]
        self.MAKE_PROGRAM = env[ "EMERGE_MAKE_PROGRAM" ]
        
    def setDirectories( self):
        """ """
        if self.COMPILER   == "msvc2005" or self.COMPILER == "msvc2008":
            self.cmakeMakefileGenerator = "NMake Makefiles"
            self.cmakeMakeProgramm      = "nmake"
        elif self.COMPILER == "mingw":
            self.cmakeMakefileGenerator = "MinGW Makefiles"
            self.cmakeMakeProgramm      = "mingw32-make"
        else:
            utils.die( "KDECOMPILER: %s not understood" % self.COMPILER )

        if self.MAKE_PROGRAM:
            self.cmakeMakeProgramm = self.MAKE_PROGRAM
            utils.debug( "set custom make program: %s" % self.MAKE_PROGRAM, 1 )

        if utils.verbose() > 1:
            print "BuildType: %s" % self.BUILDTYPE
        self.buildType = self.BUILDTYPE


        self.buildTests      = False
        self.noCopy          = False
        self.noFetch         = False
        self.noClean         = False
        self.noFast          = True
        self.buildNameExt    = None

        if self.OFFLINE    == "True":
            self.noFetch     = True
        if self.NOCOPY     == "True":
            self.noCopy      = True
        if self.NOCLEAN    == "True":
            self.noClean     = True
        if self.NOFAST    == "False":
            self.noFast      = False
        if self.BUILDTESTS == "True":
            self.buildTests  = True

        # this has to be generalized and moved into VersionSystemSourceBase.py
        self.kdesvndir       = self.KDESVNDIR
        self.kdesvnserver    = self.KDESVNSERVER
        self.kdesvnuser      = self.KDESVNUSERNAME 
        self.kdesvnpass      = self.KDESVNPASSWORD
        
        if utils.verbose() > 1 and self.repositoryPath():
            print "noCopy       : %s" % self.noCopy
            print "repositoryPath()   : %s" % self.repositoryPath().replace("/", "\\")
            
        if not ( self.noCopy and self.repositoryPath() ) :
            if self.repositoryPath():
                self.sourcePath = "..\\%s" % self.repositoryPath().split('/')[-1]
            else:
                self.sourcePath = "..\\%s" % self.instsrcdir
        else:
            self.sourcePath = "%s" % os.path.join(self.kdesvndir, self.repositoryPath() ).replace("/", "\\")
        print "sourcePath" + self.sourcePath
            
    def __unpack( self, svnpath=None, packagedir=None ):
        """fetching and copying the sources from svn"""
        if not svnpath and not packagedir:
            if self.repositoryPath():
                svnpath = self.repositoryPath()[ :self.repositoryPath().rfind('/') ]
                packagedir = self.repositoryPath()[ self.repositoryPath().rfind('/') + 1:]
            else:
                utils.die( "no svn repository information are available" )
        self.fetch( svnpath, packagedir )

        if( not os.path.exists( self.workDir() ) ):
            os.makedirs( self.workDir() )

        if not ( self.noCopy and self.repositoryPath() ):
            # now copy the tree to workdir
            srcdir  = os.path.join( self.kdesvndir, svnpath, packagedir )
            destdir = os.path.join( self.workDir(), packagedir )
            utils.copySrcDirToDestDir( srcdir, destdir )
        return True

    # is this kde or cmake specific 
    def configureDefaultDefines( self ):
        """defining the default cmake cmd line"""
        options = "\"%s\" -DCMAKE_INSTALL_PREFIX=\"%s\" " % \
              ( self.sourcePath, self.rootdir.replace( "\\", "/" ) )

        options = options + "-DCMAKE_INCLUDE_PATH=\"%s\" " % \
                os.path.join( self.rootdir, "include" ).replace( "\\", "/" )

        options = options + "-DCMAKE_LIBRARY_PATH=\"%s\" " % \
                os.path.join( self.rootdir, "lib" ).replace( "\\", "/" )

        if self.buildTests:
            options = options + " -DKDE4_BUILD_TESTS=1 "

        options = options + " -DKDE4_ENABLE_EXPERIMENTAL_LIB_EXPORT:BOOL=ON "
        options = options + " -DKDEWIN_DIR:PATH=\"%s\" " % \
               os.path.join( self.rootdir ).replace( "\\", "/" )

        return options

    def configure( self, buildType=None, customDefines="" ):
        """Using cmake"""

        self.enterBuildDir()
        
        if not self.noClean:
            utils.cleanDirectory( builddir )

        command = r"""cmake -G "%s" %s %s %s""" % \
              ( self.cmakeMakefileGenerator, \
                self.configureDefaultDefines(), \
                customDefines, \
                buildtype )

        if utils.verbose() > 0:
            print "configuration command: %s" % command
        utils.system( command ) or utils.die( "while CMake'ing. cmd: %s" % command )
        return True

    def make( self, buildType=None ):
        """Using the *make program"""
        builddir = "%s" % ( self.COMPILER )

        self.enterBuildDir()

        command = self.cmakeMakeProgramm
        # adding Targets later
        if utils.verbose() > 1:
            command += " VERBOSE=1"
        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def __install( self, buildType=None ):
        """Using *make install"""
        self.enterBuildDir()

        if utils.verbose() > 0:
            print "builddir: " + builddir

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s DESTDIR=%s install%s" % ( self.cmakeMakeProgramm, self.imageDir(), fastString ) ) or utils.die( "while installing. cmd: %s" % "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imageDir() ) )
        return True

    def compile( self, customDefines=""):
        """making all required stuff for compiling cmake based modules"""
        if( not self.buildType == None ) :
            if( not ( self.configure( self.buildType, customDefines ) and self.make( self.buildType ) ) ):
                return False
        else:
            if( not ( self.configure( "Debug", customDefines ) and self.make( "Debug" ) ) ):
                return False
            if( not ( self.configure( "Release", customDefines ) and self.make( "Release" ) ) ):
                return False
        return True

    def install( self ):
        """making all required stuff for installing cmake based modules"""
        if( not self.buildType == None ):
            if( not self.__install( self.buildType ) ):
                return False
        else:
            if( not self.__install( "debug" ) ):
                return False
            if( not self.__install( "release" ) ):
                return False
        utils.fixCmakeImageDir( self.imageDir(), self.rootdir )
        return True

    def runTest( self ):
        """running cmake based unittests"""
        self.enterBuildDir()

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True

class AutoToolsBuildSystem(BuildSystemBase):
    def __init__( self, configureOptions="", makeOptions=""):
        BuildSystemBase.__init__(self,"autotools",configureOptions,makeOptions)
        self.shell = MSysShell()
            
    def configureDefaultDefines( self ):
        """defining the default cmake cmd line"""
        return ""

    def configure( self, buildType=None, customDefines="" ):
        """configure the target"""
            
        if not self.noClean:
            utils.cleanDirectory( self.builddir )

        self.enterBuildDir()

        #todo make generic
        ret = self.shell.execute(self.sourcedir, "ruby configure", "" )
        return ret

    def make( self, buildType=None ):
        """Using the *make program"""

        self.enterBuildDir()
        
        command = "make"
        args = "-j2"
        # adding Targets later
        if utils.verbose() > 1:
            args += " VERBOSE=1"
        self.shell.execute(self.sourcedir, command, args ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def __install( self, buildType=None ):
        """Using *make install"""

        self.enterBuildDir()
        
        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s DESTDIR=%s install%s" % ( self.cmakeMakeProgramm, self.imageDir(), fastString ) ) or utils.die( "while installing. cmd: %s" % "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imageDir() ) )
        return True

    def compile( self, customDefines=""):
        """making all required stuff for compiling cmake based modules"""
        if( not self.buildType() == None ) :
            if( not ( self.configure( self.buildType(), customDefines ) and self.make( self.buildType() ) ) ):
                return False
        else:
            if( not ( self.configure( "Debug", customDefines ) and self.make( "Debug" ) ) ):
                return False
            if( not ( self.configure( "Release", customDefines ) and self.make( "Release" ) ) ):
                return False
        return True

    def install( self ):
        """making all required stuff for installing cmake based modules"""
        if( not self.buildType() == None ):
            if( not self.__install( self.buildType() ) ):
                return False
        else:
            if( not self.__install( "debug" ) ):
                return False
            if( not self.__install( "release" ) ):
                return False
        utils.fixCmakeImageDir( self.imageDir(), self.rootdir )
        return True

    def runTest( self ):
        """running cmake based unittests"""

        self.enterBuildDir()
        
        if utils.verbose() > 0:
            print "builddir: " + builddir

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True


def BuildSystemFactory(buildSystemType, source):
    """ return BuildSystemBase derived instance for recent settings"""
    utils.debug( "buildsystemFactory called for type %s" % buildSystemType, 1 )
    buildSystem = None

    if buildSystemType == None or buildSystemType == 'cmake':
        buildSystem = CMakeBuildSystem()
    elif buildSystemType == 'kde4':
        buildSystem = KDE4BuildSystem()
    elif buildSystemType == 'qmake':
        buildSystem = QMakeBuildSystem()
    elif buildSystemType == 'autotools':
        buildSystem = AutoToolsBuildSystem()
    elif buildSystemType == 'binary':
        buildSystem = BinaryBuildSystem()
    else:   
        utils.die("none or unsupported buildsystem set, use self.buildSystemType='type', where type could be 'binary', 'cmake', 'qmake', 'autotools' or 'KDE4'")
        
    buildSystem.source = source
    buildSystem.subinfo = source.subinfo
    # for cleanimage
    buildSystem.type  = buildSystemType
    # required for archive source
    source.buildSystemType = buildSystemType
    return buildSystem
