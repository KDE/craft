# -*- coding: utf-8 -*-
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
import datetime

# portage tree related
import portage

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


class baseclass:
# methods of baseclass:
# __init__                   the baseclass constructor
# execute                    called to run the derived class
# fetch                      getting the package
# unpack                     unpacking the source package
# configure                  configure the package
# make                       make the package
# compile                    compiling (configure + make) the package
# install                    installing the files into the normal
# qmerge                     mergeing the local directory to the kderoot
# unmerge                    unmergeing the local directory again
# manifest                   getting the headers
# make_package               overload this function to make the packages themselves
# setDirectories
# svnFetch                   getting sources from a custom repo url
# doPackaging
# createImportLibs           creating import libs for mingw and msvc
# stripLibs                  stripping libs
# system                     instead of using the os.system command, please use this one - it makes later changes easier


    def __init__( self, SRC_URI="", **args ):
        """ the baseclass constructor """
        if "args" in args.keys() and "env" in args["args"].keys():
            env = args["args"]["env"]
        else:
            env = dict( os.environ )
            
        if "args" in args.keys() and "argv0" in args["args"].keys():
            self.argv0 = args["args"]["argv0"]
        else:
            self.argv0 = utils.getscriptname()
            
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

        self.msys = msys_build.msys_interface()
        self.kde  = kde_build.kde_interface()
        
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

        self.setDirectories()
        
        if COMPILER == "msvc2005":
            self.compiler = "msvc2005"
        elif COMPILER == "msvc2008":
            self.compiler = "msvc2008"
        elif COMPILER == "mingw":
            self.compiler = "mingw"
        elif COMPILER == "mingw4":
            self.compiler = "mingw4"
        else:
            print >> sys.stderr, "emerge error: KDECOMPILER: %s not understood" % COMPILER
            exit( 1 )

    def execute( self, cmd=None ):
        """called to run the derived class"""
        """this will be executed from the package if the package is started on its own"""
        """it shouldn't be called if the package is imported as a python module"""
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

        self.msys.setDirectories( self.rootdir, self.imagedir, self.workdir, self.instsrcdir, self.instdestdir )
        self.kde.setDirectories( self.rootdir, self.imagedir, self.workdir, self.instsrcdir, self.instdestdir, self.subinfo )
        
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

    def cleanup( self ):
        """cleanup before install to imagedir"""
        if ( os.path.exists( self.imagedir ) ):
            utils.debug( "cleaning image dir: %s" % self.imagedir, 1 )
            utils.cleanDirectory( self.imagedir )
    
    def fetch( self ):
        """getting normal tarballs from SRC_URI"""
        utils.debug( "base fetch called", 1 )
        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True
        if len( self.subinfo.targets ) and self.subinfo.buildTarget in self.subinfo.targets.keys():
            return utils.getFiles( self.subinfo.targets[ self.subinfo.buildTarget ], self.downloaddir )
        else:
            return utils.getFiles( "", self.downloaddir )

    def git_unpack( self, repoString ):
        svndir = os.path.join( self.downloaddir, "svn-src" )
        
        ret = True
        if ( not self.noFetch ):
            safePath = os.environ["PATH"]
            os.environ["PATH"] = os.path.join(self.rootdir, "dev-utils", "git", "bin") + ";" + safePath
            if os.path.exists( self.svndir ):
                """if directory already exists, simply do a pull but obey to offline"""
                ret = self.msys.msysExecute( self.svndir, "git", "pull" )
            else:
                """it doesn't exist so clone the repo"""
                # first try to replace with a repo url from etc/portage/emergehosts.conf
                repoString = utils.replaceGitUrl( repoString )
                
                repoUrl = utils.splitGitUrl( repoString )[0]
                ret = self.msys.msysExecute( svndir, "git", "clone %s %s" % ( repoUrl, self.package ) )
            [repoUrl2, repoBranch, repoTag ] = utils.splitGitUrl( repoString )
            if ret and repoBranch:
                ret = self.msys.msysExecute( self.svndir, "git", "checkout --track -b %s origin/%s" % ( repoBranch, repoBranch ) )
            if ret and repoTag:
                ret = self.msys.msysExecute( self.svndir, "git", "checkout -b %s %s" % ( repoTag, repoTag ) )
            os.environ["PATH"] = safePath
        else:
            utils.debug( "skipping git fetch (--offline)" )
        return ret

    def unpack( self ):
        """unpacking all zipped(gz,zip,bz2) tarballs"""
        
        utils.debug( "base unpack called", 1 )

        if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
            if self.subinfo.svnTargets[ self.subinfo.buildTarget ] and utils.isGitUrl( self.subinfo.svnTargets[ self.subinfo.buildTarget ] ):
                if ( not os.path.exists( self.workdir ) ):
                    os.makedirs( self.workdir )
                return self.git_unpack( self.subinfo.svnTargets[ self.subinfo.buildTarget ] )

        if not utils.unpackFiles( self.downloaddir, self.filenames, self.workdir ):
            return False
        if len( self.subinfo.targets ) and self.subinfo.buildTarget in self.subinfo.patchToApply.keys():
            ( file, patchdepth ) = self.subinfo.patchToApply[ self.subinfo.buildTarget ]
            patchfile = os.path.join ( self.packagedir, file )
            srcdir = os.path.join ( self.workdir, self.instsrcdir )
            return utils.applyPatch( srcdir, patchfile, patchdepth )
        return True

    def compile( self ):
        """overload this function according to the packages needs"""
        utils.debug( "base compile (configure + make) called, doing nothing...", 1 )
        return True

    def configure( self ):
        """overload this function according to the packages needs"""
        utils.debug( "base configure called, doing nothing...", 1 )
        return True

    def make( self ):
        """overload this function according to the packages needs"""
        utils.debug( "base configure called, doing nothing...", 1 )
        return True

    def install( self ):
        """installing binary tarballs"""
        if utils.verbose() > 1:
            print "base install called"
        srcdir = os.path.join( self.workdir, self.instsrcdir )
        destdir = os.path.join( self.imagedir, self.instdestdir )
        utils.copySrcDirToDestDir( srcdir, destdir )
        return True

    def unittest( self ):
        """ run the unittests of the package """
        utils.debug( "currently only supported for some internal packages", 1 )
        return True

    def qmerge( self ):
        """mergeing the imagedirectory into the filesystem"""
        if utils.verbose() > 1:
            print "base qmerge called"
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packagedir, "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            destscript = os.path.join( self.imagedir, "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imagedir, "manifest" ) ):
                os.mkdir( os.path.join( self.imagedir, "manifest" ) )
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
        portage.addInstalled( self.category, self.package, self.version )
        return True

    def unmerge( self ):
        """unmergeing the files from the filesystem"""
        if utils.verbose() > 1:
            print "base unmerge called"
        utils.unmerge( self.rootdir, self.package, self.forced )
        portage.remInstalled( self.category, self.package, self.version )
        return True
        
    def manifest( self ):
        """installer compatibility: make the manifest files that make up the installers"""
        """install database"""
        if utils.verbose() > 1:
            print "base manifest called"
        utils.manifestDir( os.path.join( self.workdir, self.instsrcdir, self.package ), self.imagedir, self.category, self.package, self.version )
        return True
        
    def make_package( self ):
        """overload this function with the package specific packaging instructions"""
        if utils.verbose() > 1:
            print "currently only supported for some internal packages"
        return True

    def setDirectories( self ):
        """setting all important stuff that isn't coped with in the c'tor"""
        """parts will probably go to infoclass"""
        utils.debug( "setdirectories called", 1 )

        ( self.PV, ext ) = os.path.splitext( os.path.basename( self.argv0 ) )

        ( self.category, self.package, self.version ) = \
                       portage.getCategoryPackageVersion( self.argv0 )

        utils.debug( "setdir category: %s, package: %s" % ( self.category, self.package ) )

        self.cmakeInstallPrefix = ROOTDIR.replace( "\\", "/" )
        utils.debug( "cmakeInstallPrefix: " + self.cmakeInstallPrefix )

        if COMPILER == "msvc2005" or COMPILER == "msvc2008":
            self.cmakeMakefileGenerator = "NMake Makefiles"
            self.cmakeMakeProgramm = "nmake"
        elif COMPILER == "mingw" or COMPILER == "mingw4":
             self.cmakeMakefileGenerator = "MinGW Makefiles"
             if os.getenv("EMERGE_ARCHITECTURE") == 'x64':
                self.cmakeMakeProgramm = "gmake"
             else:
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

        self.packagedir = os.path.join( portage.rootDir(), self.category, self.package )
        self.filesdir = os.path.join( self.packagedir, "files" )
        self.kdesvndir = KDESVNDIR
        self.kdesvnserver = KDESVNSERVER
        self.kdesvnuser = KDESVNUSERNAME
        self.kdesvnpass = KDESVNPASSWORD
        self.svndir = os.path.join( self.downloaddir, "svn-src", self.package )
       
        self.strigidir = os.getenv( "STRIGI_HOME" )
        self.dbusdir = os.getenv( "DBUSDIR" )


    def svnFetch( self, repo ):
        """getting sources from a custom svn repo"""
        if utils.verbose() > 1:
            print "base svnFetch called"
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
            if not utils.unpackFiles( self.downloaddir, self.filenames, self.workdir ):
                return False
            if len( self.subinfo.targets ) and self.subinfo.buildTarget in self.subinfo.patchToApply.keys():
                ( file, patchdepth ) = self.subinfo.patchToApply[ self.subinfo.buildTarget ]
                utils.debug( "patchesToApply: %s" % file, 0 )
                patchfile = os.path.join ( self.packagedir, file )
                srcdir = os.path.join ( self.workdir, self.instsrcdir )
                return utils.applyPatch( srcdir, patchfile, patchdepth )
            return True

        
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

    def kdeTest( self ):
        return self.kde.kdeTest()

    def doPackaging( self, pkg_name, pkg_version = str( datetime.date.today() ).replace('-', ''), packSources = True, special = False ):
        """packaging according to the gnuwin32 packaging rules"""
        """this requires the kdewin-packager"""
        
        # FIXME: add a test for the installer later
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )
        binpath = os.path.join( self.imagedir, self.instdestdir )
        tmp = os.path.join( binpath, "kde" )

        patchlevel = os.getenv( "EMERGE_PKGPATCHLVL" )
        if patchlevel:
            pkg_version += "-" + patchlevel

        if( os.path.exists( tmp ) ):
            binpath = tmp
        
        if not utils.test4application( "kdewin-packager" ):
            utils.die( "kdewin-packager not found - please make sure it is in your path" )

        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packagedir, "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            destscript = os.path.join( self.imagedir, "manifest", scriptName )
            if os.path.exists( script ):
                if not os.path.exists( os.path.join( self.imagedir, "manifest" ) ):
                    os.mkdir( os.path.join( self.imagedir, "manifest" ) )
                shutil.copyfile( script, destscript )

        if ( packSources and not ( self.noCopy and self.kde.kdeSvnPath() ) ):
            srcpath = os.path.join( self.workdir, self.instsrcdir )
            cmd = "-name %s -root %s -srcroot %s -version %s -destdir %s" % \
                  ( pkg_name, binpath, srcpath, pkg_version, dstpath )
        elif packSources and self.noCopy and self.kde.kdeSvnPath():
            srcpath = os.path.join( self.kde.kdesvndir, self.kde.kdeSvnPath() ).replace( "/", "\\" )
            if not os.path.exists( srcpath ):
                srcpath = self.kde.sourcePath
            cmd = "-name %s -root %s -srcroot %s -version %s -destdir %s" % \
                  ( pkg_name, binpath, srcpath, pkg_version, dstpath )
        else:
            cmd = "-name %s -root %s -version %s -destdir %s" % \
                  ( pkg_name, binpath, pkg_version, dstpath )
        xmltemplate=os.path.join(self.packagedir,pkg_name+"-package.xml")
        if os.path.exists(xmltemplate):
            cmd = "kdewin-packager.exe " + cmd + " -template " + xmltemplate + " -notes " + "%s/%s:%s:unknown " % ( self.category, self.package, self.version ) + "-compression 2 "
        else:
            cmd = "kdewin-packager.exe " + cmd + " -notes " + "%s/%s:%s:unknown " % ( self.category, self.package, self.version ) + "-compression 2 "
        
        if( not self.createCombinedPackage ):
            if( self.compiler == "mingw"):
              cmd += " -type mingw "
            elif self.compiler == "mingw4":
              cmd += " -type mingw4 "
            elif self.compiler == "msvc2005":
              cmd += " -type msvc "
            elif self.compiler == "msvc2008":
              cmd += " -type vc90 "
            else:
              cmd += " -type unknown "

        if special:
            cmd += " -special"
        if utils.verbose:
            print "running %s" % cmd
        utils.system( cmd ) or utils.die( "while packaging. cmd: %s" % cmd )
        return True

    def createImportLibs( self, pkg_name ):
        """creating the import libraries for the other compiler(if ANSI-C libs)"""
        basepath = os.path.join( self.imagedir, self.instdestdir )
        utils.createImportLibs( pkg_name, basepath )

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
