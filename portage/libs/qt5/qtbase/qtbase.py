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
            
        for ver in self.versionInfo.tarballs() + self.versionInfo.branches() + self.versionInfo.tags():
            if ver.startswith("5.6.0"):
                self.patchToApply[ ver ] = [("qtbase-5.6.0.patch" , 1)]
            elif ver.startswith("5.6"):
                self.patchToApply[ ver ] = [("qtbase-5.6.patch" , 1)]
            elif ver.startswith("5.7"):
                self.patchToApply[ver] = [("qtbase-5.7.patch", 1)]
            else:
                self.patchToApply[ ver ] = [("qtbase-20130714.patch" , 1),]
                if ver.startswith("5.4"):
                    self.patchToApply[ ver ].append(("qmake-5.4.patch" , 1))
                if ver.startswith("5.5"):
                    self.patchToApply[ ver ] += [
                        ("qmake-5.5.patch" , 1),
                        ("0001-Fix-toDisplayString-QUrl-PreferLocalFile-on-Win.patch", 1)
                    ]
        
        self.shortDescription = "a cross-platform application framework"


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.buildDependencies['dev-util/winflexbison'] = 'default'
        if not self.options.buildStatic:
            self.dependencies['win32libs/openssl'] = 'default'
            self.dependencies['win32libs/dbus'] = 'default'
            self.dependencies['binary/mysql-pkg'] = 'default'
            self.dependencies['win32libs/icu'] = 'default'
            self.dependencies['win32libs/zlib'] = 'default'

class Package(Qt5CorePackageBase):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__(self)


    def configure( self, unused1=None, unused2=""):
        self.enterBuildDir()
        self.setPathes()
        if not os.path.exists(os.path.join(self.sourceDir(),".gitignore")):#force bootstrap of configure.exe
            with open(os.path.join(self.sourceDir(),".gitignore"),"wt+") as bootstrap:
                bootstrap.write("Force Bootstrap")
            if os.path.exists(os.path.join(self.sourceDir(),"configure.exe")):
                os.remove(os.path.join(self.sourceDir(),"configure.exe"))
        configure = os.path.join( self.sourceDir() ,"configure.bat" ).replace( "/", "\\" )
        command = " %s -opensource  -confirm-license -prefix %s -platform %s " % ( configure, EmergeStandardDirs.emergeRoot(), self.platform )
        command += "-headerdir %s " % os.path.join(EmergeStandardDirs.emergeRoot(), "include", "qt5")
        command += "-plugin-sql-odbc "
        command += "-qt-style-windowsxp  -qt-style-windowsvista "
        command += "-qt-libpng "
        command += "-qt-libjpeg "
        command += "-qt-pcre "
        command += "-nomake examples "
        # can we drop that in general?
        if not self.subinfo.buildTarget.startswith("5.7"):
            command += "-c++11 "
        command += "-opengl dynamic "
        command += "-ltcg "
        if self.buildType() == "RelWithDebInfo":
            command += "-force-debug-info "
        command += "-I \"%s\" -L \"%s\" " % (os.path.join(EmergeStandardDirs.emergeRoot(), "include"), os.path.join(EmergeStandardDirs.emergeRoot(), "lib"))

        if not self.subinfo.options.buildStatic:
            command += " -openssl-linked "
            if self.subinfo.options.isActive("binary/mysql-pkg"):
                command += " -plugin-sql-mysql "
            if self.subinfo.options.isActive("win32libs/dbus"):
                command += " -qdbus -dbus-linked "
            if self.subinfo.options.isActive("win32libs/icu"):
                command += " -icu "
            if self.subinfo.options.isActive("win32libs/zip"):
                command += " -system-zlib "
                if compiler.isMSVC():
                    command += " ZLIB_LIBS=zlib.lib "
        else:
            command += " -static -static-runtime "
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



