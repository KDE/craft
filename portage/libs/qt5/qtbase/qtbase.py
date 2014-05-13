# -*- coding: utf-8 -*-

import os

import utils
import info
import portage
import compiler
from Package.Qt5CorePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        for ver in self.versionInfo.tarballs():
            self.patchToApply[ ver ] = ("qtbase-20130714.patch" , 1)
            
        for ver in self.versionInfo.branches():
            self.patchToApply[ ver ] = ("qtbase-20130714.patch" , 1)
            
        for ver in self.versionInfo.tags():
            self.patchToApply[ ver ] = ("qtbase-20130714.patch" , 1)
            
        
        self.shortDescription = "a cross-platform application framework"


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.buildDependencies['dev-util/winflexbison'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/dbus'] = 'default'
        self.dependencies['binary/mysql-pkg'] = 'default'
        self.dependencies['win32libs/icu'] = 'default'

class Package(Qt5CorePackageBase):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__(self)
        
        # get instance of dbus and openssl package
        self.openssl = portage.getPackageInstance('win32libs', 'openssl')
        if self.subinfo.options.isActive("win32libs/dbus"):
            self.dbus = portage.getPackageInstance('win32libs', 'dbus')
        if self.subinfo.options.isActive("binary/mysql-pkg"):
            self.mysql_server = portage.getPackageInstance('binary', 'mysql-pkg')
        if self.subinfo.options.isActive("win32libs/icu"):
            self.icu = portage.getPackageInstance('win32libs','icu')


    def configure( self, unused1=None, unused2=""):
        self.enterBuildDir()
        self.setPathes()
        if not os.path.exists(os.path.join(self.sourceDir(),".gitignore")):#force bootstrap of configure.exe
            f = open(os.path.join(self.sourceDir(),".gitignore"),"wt+")
            f.write("Force Bootstrap")
            f.close()
            os.remove(os.path.join(self.sourceDir(),"configure.exe"))
        configure = os.path.join( self.sourceDir() ,"configure.bat" ).replace( "/", "\\" )
        command = " %s -opensource  -confirm-license -prefix %s -platform %s " % ( configure, EmergeStandardDirs.emergeRoot(), self.platform )
        command += "-plugin-sql-odbc "
        command += "-qt-style-windowsxp  -qt-style-windowsvista "
        command += "-qt-libpng "
        command += "-qt-libjpeg "
        command += "-qt-zlib "
        command += "-no-vcproj "
        command += "-nomake examples "
        command += "-c++11 "
        if self.buildType() == "RelWithDebInfo":
            command += "-force-debug-info "
        
        command += " -openssl-linked OPENSSL_PATH=%s " % self.openssl.installDir()
        if self.subinfo.options.isActive("binary/mysql-pkg"):
            command += " -plugin-sql-mysql MYSQL_PATH=%s " %  self.mysql_server.installDir()
        if self.subinfo.options.isActive("win32libs/dbus"):
            command += " -qdbus -dbus-linked DBUS_PATH=%s " % self.dbus.installDir()
        if self.subinfo.options.isActive("win32libs/icu"):
            command += " -icu -I \"%s\" -L \"%s\" " % (os.path.join(self.icu.imageDir(),"include"),os.path.join(self.icu.imageDir(),"lib"))
        if os.getenv("DXSDK_DIR") == None:
            command += "-opengl desktop "
        else:
            command += "-opengl es2 "
       
        command += "-ltcg "
       

        if self.buildType() == "Debug":
          command += "-debug "
        else:
          command += "-release "

        if self.supportsCCACHE:
            command != "-dont-process "
        print("command: ", command)
        if not utils.system( command ):
            return False
        if self.supportsCCACHE:
            return Qt5CorePackageBase.configure(self)
        else:
            return True
        

    def make(self, unused=''):
        self.setPathes()
        return Qt5CorePackageBase.make(self)


    def install( self ):
        self.setPathes()
        if not Qt5CorePackageBase.install(self):
            return False
        utils.copyFile( os.path.join( self.buildDir(), "bin", "qt.conf"), os.path.join( self.imageDir(), "bin", "qt.conf" ) )
            
        # install msvc debug files if available
        if compiler.isMSVC():
            srcdir = os.path.join( self.buildDir(), "lib" )
            destdir = os.path.join( self.installDir(), "lib" )

            filelist = os.listdir( srcdir )

            for file in filelist:
                if file.endswith( ".pdb" ):
                    utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ) )

        return True
        
         
         
    def setPathes( self ):
         # for building qt with qmake       
        utils.prependPath(os.path.join(self.buildDir(),"bin"))
        # so that the mkspecs can be found, when -prefix is set
        utils.putenv( "QMAKEPATH", self.sourceDir() )
        utils.putenv( "QMAKESPEC", os.path.join(self.sourceDir(), 'mkspecs', self.platform ))



