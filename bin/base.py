# this package contains the base class for all packages

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>

import sys
import os

import shutil

# for get functions etc...
import utils
# for info header class
import info
# for the msys interface
import msys_build
# for the kde interface
import kde_build
#from utils import die

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

DIRECTORYLAYOUT=os.getenv( "directory_layout" )
if ( not DIRECTORYLAYOUT == "installer" ):
    """ traditional layout is using the categories as subfolders of kderoot """
    """ installer layout has no category subfolder """
    DIRECTORYLAYOUT = "traditional"

# ok, we have the following dirs:
# ROOTDIR: the root where all this is below
# DOWNLOADDIR: the dir under rootdir, where the downloaded files are put into
# WORKDIR: the directory, under which the files are unpacked and compiled.
#            here rootdir/tmp/packagename/work
# IMAGEDIR: the directory, under which the compiled files are installed.
#            here rootdir/tmp/packagename/image


class baseclass:
# methods of baseclass:
# __init__                   the baseclass constructor
# execute                    called to run the derived class
# fetch                      getting the package
# unpack                     unpacking the source tarball
# compile                    compiling the tarball
# install                    installing the files into the normal
# qmerge                     mergeing the local directory to the kderoot
# unmerge                    unmergeing the local directory again
# manifest                   getting the headers
# make_package               overload this function to make the packages themselves
# setDirectories
# svnFetch                  getting sources from a custom repo url
# doPackaging
# createImportLibs           creating import libs for mingw and msvc
# stripLibs                  stripping libs
# system                     instead of using the os.system command, please use this one - it makes later changes easier


    def __init__( self, SRC_URI ):
        """ the baseclass constructor """
        self.SRC_URI                = SRC_URI
        self.instsrcdir             = ""
        self.instdestdir            = ""
        self.traditional            = True
        self.noCopy                 = False
        self.buildTests             = False
        self.forced                 = False
        self.versioned              = False
        self.noFetch                = False
        self.kdeCustomDefines       = ""
        self.createCombinedPackage  = False

        self.subinfo                = info.infoclass()
        self.buildTarget            = self.subinfo.defaultTarget
        self.Targets                = self.subinfo.svnTargets

        self.msys = msys_build.msys_interface()
        self.kde  = kde_build.kde_interface()
        
        if os.getenv( "EMERGE_OFFLINE" ) == "True":
            self.noFetch = True
        if os.getenv( "EMERGE_NOCOPY" ) == "True":
            self.noCopy = True
        if os.getenv( "EMERGE_FORCED" ) == "True":
            self.forced = True
        if os.getenv( "EMERGE_BUILDTESTS" ) == "True":
            self.buildTests = True
        if DIRECTORYLAYOUT == "installer":
            self.traditional = False

        # Build type for kdeCompile() / kdeInstall() - packages
        # "" -> debug and release
        Type=os.getenv( "EMERGE_BUILDTYPE" )
        if ( not Type == None ):
            if utils.verbose() > 1:
                print "BuildType: %s" % Type
            self.buildType = Type
        else:
            self.buildType = None

        if COMPILER == "msvc2005":
            self.compiler = "msvc2005"
        elif COMPILER == "mingw":
            self.compiler = "mingw"
        else:
            print "emerge error: KDECOMPILER: %s not understood" % COMPILER
            exit( 1 )

    def execute( self ):
        """called to run the derived class"""
        """this will be executed from the package if the package is started on its own"""
        """it shouldn't be called if the package is imported as a python module"""
        if utils.verbose() > 1:
            print "base exec called. args:", sys.argv

        command = sys.argv[ 1 ]
        options = ""
        if ( len( sys.argv )  > 2 ):
            options = sys.argv[ 2: ]
        if utils.verbose() > 1:
            print "command:", command
            print "opts:", options

        self.setDirectories()

        ok = True
        if command   == "fetch":       ok = self.fetch()
        elif command == "cleanimage":       self.cleanup()
        elif command == "unpack":      ok = self.unpack()
        elif command == "compile":     ok = self.compile()
        elif command == "configure":   ok = self.compile()
        elif command == "make":        ok = self.compile()
        elif command == "install":     ok = self.install()
        elif command == "qmerge":      ok = self.qmerge()
        elif command == "unmerge":     ok = self.unmerge()
        elif command == "manifest":    ok = self.manifest()
        elif command == "package":     ok = self.make_package()
        else:
            ok = utils.error( "command %s not understood" % command )

        if ( not ok ):
            utils.die( "command %s failed" % command )

    def cleanup( self ):
        """cleanup before install to imagedir"""
        if ( os.path.exists( self.imagedir ) ):
            if not utils.verbose() > 1:
                print "cleaning image dir:", self.imagedir
            utils.cleanDirectory( self.imagedir )
    
    def fetch( self ):
        """getting normal tarballs from SRC_URI"""
        if utils.verbose() > 1:
            print "base fetch called"
        if ( self.noFetch ):
            if utils.verbose() > 0:
                print "skipping fetch (--offline)"
            return True
        if len( self.subinfo.targets ) and self.subinfo.buildTarget in self.subinfo.targets.keys():
            return utils.getFiles( self.subinfo.targets[ self.subinfo.buildTarget ], self.downloaddir )
        else:
            return utils.getFiles( "", self.downloaddir ) 

    def unpack( self ):
        """unpacking all zipped(gz,zip,bz2) tarballs"""
        if utils.verbose() > 1:
            print "base unpack called, files:", self.filenames
        return utils.unpackFiles( self.downloaddir, self.filenames, self.workdir )

    def compile( self ):
        """overload this function according to the packages needs"""
        if utils.verbose() > 1:
            print "base compile called, doing nothing..."
        return True

    def install( self ):
        """installing binary tarballs"""
        if utils.verbose() > 1:
            print "base install called"
        srcdir = os.path.join( self.workdir, self.instsrcdir )
        destdir = os.path.join( self.imagedir, self.instdestdir )
        utils.copySrcDirToDestDir( srcdir, destdir )
        return True

    def qmerge( self ):
        """mergeing the imagedirectory into the filesystem"""
        if utils.verbose() > 1:
            print "base qmerge called"
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packagedir, "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            destscript = os.path.join( self.imagedir, "manifest", scriptName )
            if os.path.exists( script ):
                shutil.copyfile( script, destscript )
                             
        utils.mergeImageDirToRootDir( self.imagedir, self.rootdir )
        # run post-install scripts
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            script = os.path.join( self.rootdir, "manifest", scriptName )
            if os.path.exists( script ):
                cmd = "cd %s && %s" % ( self.rootdir, script )
                utils.system( cmd ) or utils.warning("%s failed!" % cmd )
        utils.addInstalled( self.category, self.package, self.version )
        return True

    def unmerge( self ):
        """unmergeing the files from the filesystem"""
        if utils.verbose() > 1:
            print "base unmerge called"
        utils.unmerge( self.rootdir, self.package, self.forced )
        utils.remInstalled( self.category, self.package, self.version )
        return True
        
    def manifest( self ):
        """installer compatibility: make the manifest files that make up the installers"""
        """install database"""
        if utils.verbose() > 1:
            print "base manifest called"
        utils.manifestDir( os.path.join( self.workdir, self.instsrcdir, self.package ), self.imagedir, self.package, self.version )
        return True
        
    def make_package( self ):
        """overload this function with the package specific packaging instructions"""
        if utils.verbose() > 1:
            print "currently only supported for some interal packages"
        return True

    def setDirectories( self ):
        """setting all important stuff that isn't coped with in the c'tor"""
        """parts will probably go to infoclass"""
        if utils.verbose() > 1:
            print "setdirectories called"
        #print "basename:", sys.argv[ 0 ]
        #print "src_uri", self.SRC_URI

        #print "filenames:", self.filenames

        #( self.progname, ext ) = os.path.splitext( os.path.basename( sys.argv[ 0 ] ) )
        ( self.PV, ext ) = os.path.splitext( os.path.basename( sys.argv[ 0 ] ) )
        #print "progname:", self.progname        

        ( self.category, self.package, self.version ) = \
                       utils.getCategoryPackageVersion( sys.argv[ 0 ] )

        #self.progname = self.package        
        if utils.verbose() > 0:
            print "setdir category: %s, package: %s, version: %s" %\
              ( self.category, self.package, self.version )

        self.cmakeInstallPrefix = ROOTDIR.replace( "\\", "/" )
        if utils.verbose() > 0:
            print "cmakeInstallPrefix:", self.cmakeInstallPrefix

        if COMPILER == "msvc2005":
            self.cmakeMakefileGenerator = "NMake Makefiles"
            self.cmakeMakeProgramm = "nmake"
        elif COMPILER == "mingw":
            self.cmakeMakefileGenerator = "MinGW Makefiles"
            self.cmakeMakeProgramm = "mingw32-make"
        else:
            utils.die( "KDECOMPILER: %s not understood" % COMPILER )

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
       
        self.strigidir = os.getenv( "STRIGI_HOME" )
        self.dbusdir = os.getenv( "DBUSDIR" )

        self.Targets.update( self.subinfo.svnTargets )
        self.Targets.update( self.subinfo.targets )
        
        self.subinfo.buildTarget = self.subinfo.defaultTarget

        if os.getenv( "EMERGE_TARGET" ) in self.Targets.keys():
            self.subinfo.buildTarget = os.getenv( "EMERGE_TARGET" )
            
        if self.subinfo.buildTarget in self.subinfo.targets.keys() and self.subinfo.buildTarget in self.subinfo.targetInstSrc.keys():
            self.instsrcdir = self.subinfo.targetInstSrc[ self.subinfo.buildTarget ]
#        else:
#            if self.subinfo.buildTarget in self.Targets.keys() and self.Targets[ self.subinfo.buildTarget ]:
#                self.instsrcdir = os.path.basename( self.Targets[ self.subinfo.buildTarget ] )
#            else:
#                if not self.instsrcdir:
#                    utils.warning( "Skript warning: self.instsrcdir not set - this might be ok, but if it leads to errors that might be the problem" )
            
        self.msys.setDirectories( self.rootdir, self.imagedir, self.workdir, self.instsrcdir, self.instdestdir )
        self.kde.setDirectories( self.rootdir, self.imagedir, self.workdir, self.instsrcdir, self.instdestdir, self.subinfo )
        
        if self.subinfo.buildTarget in self.subinfo.targets.keys() and not self.kdeSvnPath():
            filenames = []
            for uri in self.subinfo.targets[ self.subinfo.buildTarget ].split():
                filenames.append( os.path.basename( uri ) )
            self.filenames = filenames
            


    def svnFetch( self, repo ):
        """getting sources from a custom svn repo"""
        if utils.verbose() > 1:
            print "base svnFetch called"
        self.svndir = os.path.join( self.downloaddir, "svn-src", self.package )
        if ( self.noFetch ):
            if utils.verbose() > 0:
                print "skipping svn fetch/update (--offline)"
            return True
        
        utils.svnFetch( repo, self.svndir )

    def kdeGet( self ):
        return self.kdeSvnPath()

    def __kdesinglecheckout( self, repourl, ownpath, codir, doRecursive = False ):
        self.kde.kdesinglecheckout( repourl, ownpath, codir, doRecursive )
                
    def kdeSvnFetch( self, svnpath, packagedir ):
        return self.kde.kdeSvnFetch( svnpath, packagedir )

    def kdeSvnPath( self ):
        return self.kde.kdeSvnPath()
        
    def kdeSvnUnpack( self, svnpath=None, packagedir=None ):
        if self.kde.kdeSvnPath():
            return self.kde.kdeSvnUnpack( svnpath, packagedir )
        else:
            return utils.unpackFiles( self.downloaddir, self.filenames, self.workdir )
        
    def kdeDefaultDefines( self ):
        return self.kde.kdeDefaultDefines()

    def kdeConfigureInternal( self, buildType ):
        return self.kde.kdeConfigureInternal( buildType, self.kdeCustomDefines )

    def kdeMakeInternal( self, buildType ):
        return self.kde.kdeMakeInternal( buildType )
    
    def kdeInstallInternal( self, buildType ):
        return self.kde.kdeInstallInternal( buildType )

    def kdeCompile( self ):
        return self.kde.kdeCompile( self.kdeCustomDefines )

    def kdeInstall( self ):
        return self.kde.kdeInstall()

    def doPackaging( self, pkg_name, pkg_version, packSources = True ):
        """packaging according to the gnuwin32 packaging rules"""
        """this requires the kdewin-packager"""
        
        # FIXME: add a test for the installer later
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )
        binpath = os.path.join( self.imagedir, self.instdestdir )
        tmp = os.path.join( binpath, "kde" )

        if( os.path.exists( tmp ) ):
            binpath = tmp
        
        if not utils.test4application( "kdewin-packager" ):
            utils.die( "kdewin-packager not found - please make sure it is in your path" )

        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packagedir, "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            destscript = os.path.join( self.imagedir, "manifest", scriptName )
            if os.path.exists( script ):
                shutil.copyfile( script, destscript )

        if ( packSources and not ( self.noCopy and self.kde.kdeSvnPath() ) ):
            srcpath = os.path.join( self.workdir, self.instsrcdir )
            cmd = "-name %s -root %s -srcroot %s -version %s -destdir %s" % \
                  ( pkg_name, binpath, srcpath, pkg_version, dstpath )
        elif self.noCopy and self.kde.kdeSvnPath():
            srcpath = os.path.join(self.kde.kdesvndir, self.kde.kdeSvnPath() ).replace( "/", "\\" )
            cmd = "-name %s -root %s -srcroot %s -version %s -destdir %s" % \
                  ( pkg_name, binpath, srcpath, pkg_version, dstpath )
        else:
            cmd = "-name %s -root %s -version %s -destdir %s" % \
                  ( pkg_name, binpath, pkg_version, dstpath )
        cmd = "kdewin-packager.exe -debuglibs " + cmd + " -compression 2 "

        if( not self.createCombinedPackage ):
            if( self.compiler == "mingw"):
              cmd = cmd + " -type mingw "
            else:
              cmd = cmd + " -type msvc "

        utils.system( cmd ) or utils.die("while packaging. cmd: %s" % cmd)
        return True

    def createImportLibs( self, pkg_name ):
        """creating the import libraries for the other compiler(if ANSI-C libs)"""
        basepath = os.path.join( self.imagedir, self.instdestdir )

        dst = os.path.join( basepath, "lib" )
        if( not os.path.exists( dst ) ):
            os.mkdir( dst )

        dllpath = os.path.join( basepath, "bin", "%s.dll" % pkg_name )
        defpath = os.path.join( basepath, "lib", "%s.def" % pkg_name )
        imppath = os.path.join( basepath, "lib", "%s.lib" % pkg_name )
        gccpath = os.path.join( basepath, "lib", "%s.dll.a" % pkg_name )

        # create .def
        cmd = "pexports %s > %s " % ( dllpath, defpath )
        self.system( cmd )

        if( not os.path.isfile( imppath ) ):
            # create .lib
            cmd = "lib /machine:x86 /def:%s /out:%s" % ( defpath, imppath )
            self.system( cmd )
        
        if( not os.path.isfile( gccpath ) ):
            # create .dll.a
            cmd = "dlltool -d %s -l %s" % ( defpath, gccpath )
            self.system( cmd )
        return True

    def stripLibs( self, pkg_name ):
        """stripping libraries"""
        basepath = os.path.join( self.imagedir, self.instdestdir )
        dllpath = os.path.join( basepath, "bin", "%s.dll" % pkg_name )

        cmd = "strip -s " + dllpath
        self.system( cmd )
        return True

    def msysConfigureFlags( self ):
        return self.msys.msysConfigureFlags()

    def msysCompile( self, bOutOfSource = True ):
        return self.msys.msysCompile( bOutOfSource )

    def msysInstall( self, bOutOfSource = True ):
        return self.msys.msysInstall( bOutOfSource )

    def system( self, command , infileName = None, outfileName = os.path.join( ROOTDIR, "out.log" ), errfileName = os.path.join( ROOTDIR, "out.log" ) ):
        """this function should be called instead of os.system it will return the errorstatus"""
        """and take the name of a possible command file and the names of stdout and stderr"""
        """logfiles. it should be called  """
        utils.system( command ) or utils.die( "os.system ( %s ) failed" % command )
        return True

# ############################################################################################
# for testing purpose only:
# ############################################################################################
if __name__ == '__main__':
    if utils.verbose() > 0:    
        print "KDEROOT:     ", ROOTDIR
        print "KDECOMPILER: ", COMPILER
        print "DOWNLOADDIR: ", DOWNLOADDIR
        print "KDESVNDIR:   ", KDESVNDIR
        print "KDESVNSERVER:", KDESVNSERVER
        print "MSYSDIR:", MSYSDIR
    
    test = baseclass()
    test.system( "dir" )
