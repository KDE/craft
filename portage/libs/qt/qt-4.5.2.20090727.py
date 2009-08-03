# -*- coding: utf-8 -*-
import base
import utils
import shutil
from utils import die
import os
import info
import re

from Package.QMakePackageBase import *

# ok we need something more here
# dbus-lib
# openssl-lib
# we can't use kde-root/include because we get conflicting includes then
# we have to make sure that the compiler picks up the correct ones!
# --> fetch the two libs above, unpack them into a separate folder

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.4.3-3'] = 'branches/qt/4.4'
        self.svnTargets['4.5.1-1'] = 'trunk/qt-copy/'
        self.svnTargets['static'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.5.2-patched|v4.5.2"
        self.svnTargets['master'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git"
        self.svnTargets['4.5.2-patched'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.5.2-patched|v4.5.2"
        self.defaultTarget = '4.5.2-patched'
        ## \todo this is prelimary  and may be changed 
        self.options.package.fileName = 'qt'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        # for compiling qt is only mysql-embedded is really required 
        # mysql-server would also work but is much bigger 
        self.hardDependencies['testing/mysql-embedded'] = 'default'
        if COMPILER == "mingw":
            self.hardDependencies['win32libs-bin/dbus'] = 'default'
        else:
            self.hardDependencies['win32libs-sources/dbus-src'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'

class Package(QMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__(self)
        # get instance of dbus and openssl package
        if self.compiler() == "mingw":
            self.dbus = utils.getPackageInstance('win32libs-bin','dbus')
        else:
            self.dbus = utils.getPackageInstance('win32libs-sources','dbus-src')
        self.openssl = utils.getPackageInstance('win32libs-bin','openssl')
        self.mysql = utils.getPackageInstance('testing','mysql-embedded')

    def configure( self, unused1=None, unused2=""):
        self.enterBuildDir()

        # 
        os.putenv( "PATH", os.path.join( self.buildDir(), "bin" ) + ";" + os.getenv("PATH") )

        # so that the mkspecs can be found, when -prefix is set
        os.putenv( "QMAKEPATH", self.sourceDir() )

        platform = ""
        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008":
            platform = "win32-%s" % self.compiler()
        elif self.compiler() == "mingw":
            platform = "win32-g++"
        else:
            exit( 1 )

        os.environ[ "USERIN" ] = "y"
        userin = "y"

        incdirs =  " -I \"" + os.path.join( self.dbus.installDir(), "include" ) + "\""
        libdirs =  " -L \"" + os.path.join( self.dbus.installDir(), "lib" ) + "\""
        incdirs += " -I \"" + os.path.join( self.openssl.installDir(), "include" ) + "\""
        libdirs += " -L \"" + os.path.join( self.openssl.installDir(), "lib" ) + "\""
        incdirs += " -I \"" + os.path.join( self.mysql.installDir(), "include" ) + "\""
        libdirs += " -L \"" + os.path.join( self.mysql.installDir(), "lib" ) + "\""
        
        configure = os.path.join( self.sourceDir(), "configure.exe" ).replace( "/", "\\" )
        command = r"echo %s | %s -opensource -platform %s -prefix %s " \
          "-qt-gif -qt-libpng -qt-libjpeg -qt-libtiff -plugin-sql-mysql " \
          "-no-phonon -qdbus -openssl -dbus-linked " \
          "-fast -no-vcproj -no-dsp " \
          "-nomake demos -nomake examples -nomake docs " \
          "%s %s" % ( userin, configure, platform, self.installDir(), incdirs, libdirs)
        if self.buildType() == "Debug":
          command += " -debug "
        else:
          command += " -release "
        print "command: ", command
        utils.system( command )
        return True        
        
    def make(self, unused=''):
        libtmp = os.getenv( "LIB" )
        inctmp = os.getenv( "INCLUDE" )

        incdirs =  ";" + os.path.join( self.dbus.installDir(), "include" )
        libdirs =  ";" + os.path.join( self.dbus.installDir(), "lib" )
        incdirs += ";" + os.path.join( self.openssl.installDir(), "include" )
        libdirs += ";" + os.path.join( self.openssl.installDir(), "lib" )
        incdirs += ";" + os.path.join( self.mysql.installDir(), "include" )
        libdirs += ";" + os.path.join( self.mysql.installDir(), "lib" )
        print incdirs
        print libdirs
        os.environ[ "INCLUDE" ] = "%s%s" % (inctmp, incdirs)
        os.environ[ "LIB" ] = "%s%s" % (libtmp, libdirs)
        
        # so that the mkspecs can be found, when -prefix is set
        os.putenv( "QMAKEPATH", self.sourceDir() )

        QMakeBuildSystem.make(self)
        
        os.environ[ "LIB" ] = libtmp
        os.environ[ "INCLUDE" ] = inctmp
      

    def install( self ):
        if not QMakeBuildSystem.install(self):
            return False

        # create qt.conf 
        utils.copyFile( os.path.join( self.packageDir(), "qt.conf" ), os.path.join( self.installDir(), "bin", "qt.conf" ) )
        
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
