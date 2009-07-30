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
        ## \todo this is prelimary  and may be changed 
        self.options.package.fileName = 'qt'

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
        if self.compiler() == "msvc2005":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-msvc-1.2.4-1-lib.tar.bz2"
        elif self.compiler() == "msvc2008":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-vc90-1.2.4-1-lib.tar.bz2"
        elif self.compiler() == "mingw":
            self.dbuslib = "http://downloads.sourceforge.net/kde-windows/dbus-mingw-1.2.4-1-lib.tar.bz2"
        self.subinfo = subinfo()

    def fetch(self):
        if not GitSource.fetch(self):
            return False
            
        if not utils.getFile(self.openssl,self.downloadDir()):
            return False

        if not utils.getFile(self.dbuslib,self.downloadDir()):
            return False
            
        return True
        
    def unpack( self ):
        utils.cleanDirectory( self.buildDir() )

        self.enterBuildDir()
        
        thirdparty_dir = os.path.join( self.buildDir(), "3rdparty" )

        utils.createDir(thirdparty_dir)
        if not utils.unpackFile( self.downloadDir(), os.path.basename(self.openssl), thirdparty_dir ):
            return False

        if not utils.unpackFile( self.downloadDir(), os.path.basename(self.dbuslib), thirdparty_dir ):
            return False

        return True

    # def compile(self): is no more defined in packages. It is defined in BuildSystemBase.py 
    # and is a wrapper for configure and make. Having only one task in a method makes it possible 
    # to continue make after a make error  without the need to reconfigùre the whole package, 
    # which needs much time for big packages
    
    def configure( self, buildType=None, defines=""):
        thirdparty_dir = os.path.join( self.buildDir(), "3rdparty" )
        os.putenv( "PATH", os.path.join( self.buildDir(), "bin" ) + ";" + os.getenv("PATH") )
        configure = os.path.join( self.sourceDir(), "configure.exe" ).replace( "/", "\\" )

        self.enterBuildDir()

        # so that the mkspecs can be found, when -prefix is set
        os.putenv( "QMAKEPATH", self.sourceDir() )

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

        command = r"echo %s | %s -opensource -platform %s -prefix %s " \
          "-qt-gif -qt-libpng -qt-libjpeg -qt-libtiff " \
          "-no-phonon -qdbus -openssl -dbus-linked " \
          "-fast -no-vcproj -no-dsp " \
          "-nomake demos -nomake examples -nomake docs " \
          "-I \"%s\" -L \"%s\" " % \
          ( userin, configure, platform, prefix,
            os.path.join( thirdparty_dir, "include" ),
            os.path.join( thirdparty_dir, "lib" ) )
        if self.buildType() == "Debug":
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
        QMakeBuildSystem.install(self)

        # create qt.conf 
        src = os.path.join( self.packageDir(), "qt.conf" )
        dst = os.path.join( self.installDir(), "bin", "qt.conf" )
        shutil.copy( src, dst )
        
        # install msvc debug files if available
        if self.buildType() == "Debug" and (self.compiler() == "msvc2005" or self.compiler() == "msvc2008"):
            srcdir = os.path.join( self.buildDir(), "lib" )
            destdir = os.path.join( self.installDir(), "lib" )

            filelist = os.listdir( srcdir )
            
            for file in filelist:
                if file.endswith( ".pdb" ):
                    shutil.copy( os.path.join( srcdir, file ), os.path.join( destdir, file ) )
                
        return True

    #def make_package( self ):
    #    #return self.doPackaging( "qt", self.buildTarget, True, True )

if __name__ == '__main__':
    Package().execute()
