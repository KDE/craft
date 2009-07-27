# -*- coding: utf-8 -*-
import base
import utils
import shutil
from utils import die
import os
import info
import re

from Source.GitSource import *
from BuildSystem.QMakeBuildSystem import *
from Package.PackageBase import *
from Packager.KDEWinPackager import *

# ok we need something more here
# dbus-lib
# openssl-lib
# we can't use kde-root/include because we get conflicting includes then
# we have to make sure that the compiler picks up the correct ones!
# --> fetch the two libs above, unpack them into a separate folder

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['static'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.5.2-patched|v4.5.2"
        self.svnTargets['master'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git"
        self.svnTargets['4.5.2-patched'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.5.2-patched|v4.5.2"
        self.defaultTarget = '4.5.2-patched'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        # the dbus binary package do not contain debug import libraries
        if os.getenv("KDECOMPILER") == "mingw":
            self.hardDependencies['win32libs-bin/dbus'] = 'default'
        else:
            self.hardDependencies['win32libs-sources/dbus-src'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'

# the dbus and openssl dependencies are not important to be installed, but
# rather that the packages have been downloaded for use in this build
# check that 

class Package(PackageBase, GitSource, QMakeBuildSystem, KDEWinPackager):
    def __init__( self, **args ):
        GitSource.__init__(self)
        QMakeBuildSystem.__init__(self)
        PackageBase.__init__(self)
        KDEWinPackager.__init__(self)
        
        self.openssl = "http://downloads.sourceforge.net/kde-windows/openssl-0.9.8k-3-lib.tar.bz2"
        if self.compiler == "msvc2005":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-msvc-1.2.4-1-lib.tar.bz2"
        elif self.compiler == "msvc2008":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-vc90-1.2.4-1-lib.tar.bz2"
        elif self.compiler == "mingw":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-mingw-1.2.4-1-lib.tar.bz2"
        self.subinfo = subinfo()

    # in def fetch(self): git sources are fetched 
    
    def unpack( self ):
        utils.cleanDirectory( self.workdir )

        # copy include header and libs into local work dir
        if not os.path.exists( os.path.join( self.workdir, "3rdparty", "include", "dbus" ) ):
            os.makedirs( os.path.join( self.workdir, "3rdparty", "include", "dbus" ) )
        utils.copySrcDirToDestDir( os.path.join( self.rootdir, "include", "dbus" ), os.path.join( self.workdir, "3rdparty", "include", "dbus" ) )
        if not os.path.exists( os.path.join( self.workdir, "3rdparty", "include", "openssl" ) ):
            os.makedirs( os.path.join( self.workdir, "3rdparty", "include", "openssl" ) )
        utils.copySrcDirToDestDir( os.path.join( self.rootdir, "include", "openssl" ), os.path.join( self.workdir, "3rdparty", "include", "openssl" ) )

        if not os.path.exists( os.path.join( self.workdir, "3rdparty", "lib" ) ):
            os.makedirs( os.path.join( self.workdir, "3rdparty", "lib" ) )
        re1 = re.compile(".*dbus-1.*")
        re2 = re.compile(".*eay.*")
        for filename in os.listdir( os.path.join( self.rootdir, "lib" ) ):
            if re1.match( filename ) or re2.match( filename ):
                src = os.path.join( self.rootdir, "lib", filename )
                dst = os.path.join( self.workdir, "3rdparty", "lib", filename )
                shutil.copyfile( src, dst )

        return True

    def configure( self, buildType=None, defines=""):
        print "configure called"
        qtsrcdir = self.sourceDir()
        qtbindir = self.workdir
        thirdparty_dir = os.path.join( self.workdir, "3rdparty" )

        os.putenv( "PATH", os.path.join( qtbindir, "bin" ) + ";" + os.getenv("PATH") )

        configure = os.path.join( qtsrcdir, "configure.exe" ).replace( "/", "\\" )

        if not os.path.exists( qtbindir ):
          os.mkdir( qtbindir )
        os.chdir( qtbindir )

        # so that the mkspecs can be found, when -prefix is set
        os.putenv( "QMAKEPATH", qtsrcdir )

        # configure qt
        # prefix = os.path.join( self.rootdir, "qt" ).replace( "\\", "/" )
        prefix = self.installDir()
        platform = ""
        libtmp = os.getenv( "LIB" )
        inctmp = os.getenv( "INCLUDE" )
        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008":
            platform = "win32-%s" % self.compiler()
        elif self.compiler() == "mingw":
            os.environ[ "LIB" ] = ""
            os.environ[ "INCLUDE" ] = ""
            platform = "win32-g++"
        else:
            exit( 1 )

        os.environ[ "USERIN" ] = "y"
        userin = "y"
        os.chdir( qtbindir )
        command = r"echo %s | %s -opensource -platform %s -prefix %s " \
          "-qt-gif -qt-libpng -qt-libjpeg -qt-libtiff " \
          "-no-phonon -qdbus -openssl -dbus-linked " \
          "-fast -no-vcproj -no-dsp " \
          "-nomake demos -nomake examples -nomake docs " \
          "-I \"%s\" -L \"%s\" " % \
          ( userin, configure, platform, prefix,
            os.path.join( thirdparty_dir, "include" ),
            os.path.join( thirdparty_dir, "lib" ) )
        if self.buildType == "Debug":
          command = command + " -debug "
        else:
          command = command + " -release "
        print "command: ", command
        utils.system( command )
        
        if( not libtmp == None ):
            os.environ[ "LIB" ] = libtmp
        if( not inctmp == None ):
            os.environ[ "INCLUDE" ] = inctmp

        return True        

    def install( self ):
        qtbindir = os.path.join( self.workdir, self.instsrcdir )
        os.putenv( "PATH", os.path.join( qtbindir, "bin" ) + ";" + os.getenv("PATH") )

        os.chdir( os.path.join( self.workdir, self.instsrcdir ) )
        self.system( "%s install" % self.cmakeMakeProgramm )

        src = os.path.join( self.packagedir, "qt.conf" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "qt.conf" )
        shutil.copy( src, dst )
        
        if self.buildType == "Debug" and (self.compiler == "msvc2005" or self.compiler == "msvc2008"):
            srcdir = os.path.join( self.workdir, self.instsrcdir, "lib" )
            destdir = os.path.join( self.imagedir, self.instdestdir, "lib" )

            filelist = os.listdir( srcdir )
            
            for file in filelist:
                if file.endswith( ".pdb" ):
                    shutil.copy( os.path.join( srcdir, file ), os.path.join( destdir, file ) )
                
        return True

    def make_package( self ):
        return self.doPackaging( "qt", self.buildTarget, True, True )

if __name__ == '__main__':
    Package().execute()
