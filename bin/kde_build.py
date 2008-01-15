# definitions for the kde build system (cmake and svn)
import os
import utils

import base
import info

COMPILER            = os.getenv( "KDECOMPILER" )
KDESVNUSERNAME      = os.getenv( "KDESVNUSERNAME" )
KDESVNPASSWORD      = os.getenv( "KDESVNPASSWORD" )
KDESVNDIR           = os.getenv( "KDESVNDIR" )
KDESVNSERVER        = os.getenv( "KDESVNSERVER" )
if ( KDESVNDIR    == None ):
    KDESVNDIR       = os.path.join( DOWNLOADDIR, "svn-src", "kde" )
if ( KDESVNSERVER == None ):
    KDESVNSERVER    = "svn://anonsvn.kde.org"
BUILDTYPE           = os.getenv( "EMERGE_BUILDTYPE" )
if ( BUILDTYPE not in ["Debug", "Release", "RelWithDebInfo", "MinSizeRel"] ):
    BUILDTYPE=None

class kde_interface:
#    def __init__( self ):
        

    def setDirectories( self, rootdir, imagedir, workdir, instsrcdir, instdestdir, infoobject ):
        """ """
        self.subinfo = infoobject

        if COMPILER   == "msvc2005":
            self.cmakeMakefileGenerator = "NMake Makefiles"
            self.cmakeMakeProgramm      = "nmake"
        elif COMPILER == "mingw":
            self.cmakeMakefileGenerator = "MinGW Makefiles"
            self.cmakeMakeProgramm      = "mingw32-make"
        else:
            utils.die( "KDECOMPILER: %s not understood" % COMPILER )

        if utils.verbose() > 1:
            print "BuildType: %s" % BUILDTYPE
        self.buildType = BUILDTYPE


        self.buildTests      = False
        self.noCopy          = False
        self.noFetch         = False
        self.noClean         = False
        self.traditional     = True

        self.rootdir         = rootdir
        self.workdir         = workdir
        self.imagedir        = imagedir
        self.instsrcdir      = instsrcdir
        self.instdestdir     = instdestdir

        if os.getenv( "EMERGE_OFFLINE" )    == "True":
            self.noFetch     = True
        if os.getenv( "EMERGE_NOCOPY" )     == "True":
            self.noCopy      = True
        if os.getenv( "EMERGE_NOCLEAN" )    == "True":
            self.noClean     = True
        if os.getenv( "EMERGE_BUILDTESTS" ) == "True":
            self.buildTests  = True
        if os.getenv( "directory_layout" )  == "installer":
            self.traditional = False

        self.kdesvndir       = KDESVNDIR
        self.kdesvnserver    = KDESVNSERVER
        self.kdesvnuser      = KDESVNUSERNAME
        self.kdesvnpass      = KDESVNPASSWORD

    def kdesinglecheckout( self, repourl, ownpath, codir, doRecursive = False ):
        """in ownpath try to checkout codir from repourl """
        """if codir exists and doRecursive is false, simply return,"""
        """if codir does not exist, but ownpath/.svn exists,"""
        """   do a svn update codir"""
        """else do svn co repourl/codir"""
        """if doRecursive is false, add -N to the svn command """

        if ( os.path.exists( os.path.join( ownpath, codir ) ) and not doRecursive ):
            if utils.verbose() > 0:
                print "ksco exists:", ownpath, codir
            return

        if ( doRecursive ):
                recFlag = ""
        else:
                recFlag = "-N"

        if ( os.path.exists( os.path.join( ownpath, ".svn" ) ) ):
            # svn up
            svncmd = "svn update %s %s" % ( recFlag, codir )
        else:
            #svn co
            svncmd = "svn checkout %s %s" % ( recFlag, repourl + codir )

        if utils.verbose() > 1:
            print "kdesinglecheckout:pwd ", ownpath
            print "kdesinglecheckout:   ", svncmd
        os.chdir( ownpath )
        utils.system( svncmd ) or utils.die( "while checking out. cmd: %s" % svncmd )

    def kdeSvnFetch( self, svnpath, packagedir ):
        """svnpath is the part of the repo url after /home/kde, for example"""
        """"trunk/kdesupport/", which leads to the package itself,"""
        """without the package"""

        if utils.verbose() > 1:
            print "kdeSvnFetch called. svnpath: %s dir: %s" % ( svnpath, packagedir )

        if ( self.noFetch ):
            if utils.verbose() > 0:
                print "skipping svn fetch/update (--offline)"
            return True

        svndir = self.kdesvndir
        if ( not os.path.exists( svndir ) ):
                os.mkdir( svndir )

        repourl = self.kdesvnserver + "/home/kde/"

        for tmpdir in svnpath.split( "/" ):
            if ( tmpdir == "" ):
                    continue
            if utils.verbose() > 1:
                print "  svndir: %s" % svndir
                print "  dir to checkout: %s" % tmpdir
                print "  repourl", repourl

            self.kdesinglecheckout( repourl, svndir, tmpdir, False )
            svndir = os.path.join( svndir, tmpdir )
            repourl = repourl + tmpdir + "/"

        if utils.verbose() > 0:
            print "dir in which to really checkout: %s" % svndir
            print "dir to really checkout: %s" % packagedir
        self.kdesinglecheckout( repourl, svndir, packagedir, True )

        svndir = os.path.join( self.kdesvndir, svnpath ).replace( "/", "\\" )
        #repo = self.kdesvnserver + "/home/kde/" + svnpath + dir
        #utils.svnFetch( repo, svndir, self.kdesvnuser, self.kdesvnpass )
        if utils.verbose() > 1:
            print "kdesvndir", self.kdesvndir
            print "svndir", svndir
        self.svndir = os.path.join( svndir, packagedir )

        return True

    def kdeSvnPath( self ):
        """overload this function in kde packages to use the nocopy option"""
        """this function should return the full path seen from /home/KDE/"""
        return self.subinfo.svnTargets[ self.subinfo.buildTarget ]

    def kdeSvnUnpack( self, svnpath=None, packagedir=None ):
        """fetching and copying the sources from svn"""
        if not svnpath and not packagedir:
            if self.kdeSvnPath():
                svnpath = self.kdeSvnPath()[ :self.kdeSvnPath().rfind('/') ]
                packagedir = self.kdeSvnPath()[ self.kdeSvnPath().rfind('/') + 1:]
            else:
                utils.die( "no svn repository information are available" )
        self.kdeSvnFetch( svnpath, packagedir )

        if( not os.path.exists( self.workdir ) ):
            os.makedirs( self.workdir )

        if not ( self.noCopy and self.kdeSvnPath() ):
            # now copy the tree to workdir
            srcdir  = os.path.join( self.kdesvndir, svnpath, packagedir )
            destdir = os.path.join( self.workdir, packagedir )
            utils.copySrcDirToDestDir( srcdir, destdir )
        return True

    def kdeDefaultDefines( self ):
        """defining the default cmake cmd line"""
        #FIXME: can we define the paths externally???
        if utils.verbose() > 1 and self.kdeSvnPath():
            print "noCopy       : %s" % self.noCopy
            print "kdeSvnPath() : %s" % self.kdeSvnPath().replace("/", "\\")
        if not ( self.noCopy and self.kdeSvnPath() ) :
            source_path = "..\\%s" % self.instsrcdir
        else:
            source_path = "%s" % os.path.join(self.kdesvndir, self.kdeSvnPath() ).replace("/", "\\")
#        if( not self.instsrcdir == "" ):
#            source_path = self.instsrcdir
        if self.traditional:
            options = "%s -DCMAKE_INSTALL_PREFIX=%s/kde " % \
                  ( source_path, self.rootdir.replace( "\\", "/" ) )

            options = options + "-DCMAKE_INCLUDE_PATH=%s;%s " % \
                    ( os.path.join( self.rootdir, "win32libs", "include" ).replace( "\\", "/" ), \
                      os.path.join( self.rootdir, "kde", "include" ).replace( "\\", "/" ) \
                    )

            options = options + "-DCMAKE_LIBRARY_PATH=%s;%s " % \
                    ( os.path.join( self.rootdir, "win32libs", "lib" ).replace( "\\", "/" ), \
                      os.path.join( self.rootdir, "kde", "lib" ).replace( "\\", "/" ) \
                    )
        else:
            options = "%s -DCMAKE_INSTALL_PREFIX=%s " % \
                  ( source_path, self.rootdir.replace( "\\", "/" ) )

            options = options + "-DCMAKE_INCLUDE_PATH=%s " % \
                    os.path.join( self.rootdir, "include" ).replace( "\\", "/" )

            options = options + "-DCMAKE_LIBRARY_PATH=%s " % \
                    os.path.join( self.rootdir, "lib" ).replace( "\\", "/" )

        if self.buildTests:
            options = options + " -DKDE4_BUILD_TESTS=1 "

        options = options + "-DKDEWIN_DIR:PATH=%s" % \
               os.path.join( self.rootdir ).replace( "\\", "/" )

        return options

    def kdeConfigureInternal( self, buildType, kdeCustomDefines ):
        """Using cmake"""
        builddir = "%s" % ( COMPILER )

        if( not buildType == None ):
            buildtype = "-DCMAKE_BUILD_TYPE=%s" % buildType
            builddir = "%s-%s" % ( builddir, buildType )

        if not self.noClean:
            os.chdir( self.workdir )
            utils.cleanDirectory( builddir )
        os.chdir( builddir )

        command = r"""cmake -G "%s" %s %s %s""" % \
              ( self.cmakeMakefileGenerator, \
                self.kdeDefaultDefines(), \
                kdeCustomDefines, \
                buildtype )

        if utils.verbose() > 0:
            print "configuration command: %s" % command
        utils.system( command ) or utils.die( "while CMake'ing. cmd: %s" % command )
        return True

    def kdeMakeInternal( self, buildType ):
        """Using the *make program"""
        builddir = "%s" % ( COMPILER )

        if( not buildType == None ):
            buildtype = "-DCMAKE_BUILD_TYPE=%s" % buildType
            builddir = "%s-%s" % ( builddir, buildType )

        os.chdir( os.path.join( self.workdir, builddir ) )
        command = self.cmakeMakeProgramm
        # adding Targets later
        if utils.verbose() > 1:
            command += " VERBOSE=1"
        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def kdeInstallInternal( self, buildType ):
        """Using *make install"""
        builddir = "%s" % ( COMPILER )

        if( not buildType == None ):
            builddir = "%s-%s" % ( builddir, buildType )

        os.chdir( self.workdir )
        os.chdir( builddir )
        if utils.verbose() > 0:
            print "builddir: " + builddir

        utils.system( "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imagedir ) ) or utils.die( "while installing. cmd: %s" % "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imagedir ) )
        return True

    def kdeCompile( self, kdeCustomDefines ):
        """making all required stuff for compiling cmake based modules"""
        if( not self.buildType == None ) :
            if( not ( self.kdeConfigureInternal( self.buildType, kdeCustomDefines ) and self.kdeMakeInternal( self.buildType ) ) ):
                return False
        else:
            if( not ( self.kdeConfigureInternal( "Debug", kdeCustomDefines ) and self.kdeMakeInternal( "Debug" ) ) ):
                return False
            if( not ( self.kdeConfigureInternal( "Release", kdeCustomDefines ) and self.kdeMakeInternal( "Release" ) ) ):
                return False
        return True

    def kdeInstall( self ):
        """making all required stuff for installing cmake based modules"""
        if( not self.buildType == None ):
            if( not self.kdeInstallInternal( self.buildType ) ):
                return False
        else:
            if( not self.kdeInstallInternal( "debug" ) ):
                return False
            if( not self.kdeInstallInternal( "release" ) ):
                return False
        utils.fixCmakeImageDir( self.imagedir, self.rootdir )
        return True

