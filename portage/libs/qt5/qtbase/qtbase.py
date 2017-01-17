# -*- coding: utf-8 -*-

import os

import utils
import info
import portage
import compiler
from CraftOS.osutils import OsUtils
from Package.Qt5CorePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        for ver in self.versionInfo.tarballs() + self.versionInfo.branches() + self.versionInfo.tags():
            qtVer = CraftVersion(ver)
            if ver == "dev":
                self.patchToApply[ver] = [
                    ("fix-angle-mingw.patch", 1),
                    ("qtbase-5.8.patch", 1),#https://codereview.qt-project.org/#/c/141254/
                                            #https://codereview.qt-project.org/#/c/149550/
                ]
            elif qtVer >= CraftVersion("5.8"):
                self.patchToApply[ver] = [
                    ("fix-angle-mingw.patch", 1),
                    ("qtbase-5.8.patch", 1),  # https://codereview.qt-project.org/#/c/141254/
                    # https://codereview.qt-project.org/#/c/149550/
                    ("qdbus-manager-quit-5.8.patch", 1)  # https://phabricator.kde.org/D2545#69186
                ]
            elif qtVer >= CraftVersion("5.7"):
                self.patchToApply[ver] = [
                    ("fix-angle-mingw.patch", 1),
                    ("qtbase-5.7.patch", 1),  # https://codereview.qt-project.org/#/c/141254/
                    # https://codereview.qt-project.org/#/c/149550/
                    ("do-not-spawn-console-qprocess-startdetached.patch", 1),
                    # https://codereview.qt-project.org/#/c/162585/
                    ("qdbus-manager-quit-5.7.patch", 1)  # https://phabricator.kde.org/D2545#69186
                ]
            else:
                self.patchToApply[ ver ] = [
                    ("qmake-fix-install-root.patch", 1),
                    ("qtbase-5.6.patch" , 1),#https://codereview.qt-project.org/#/c/141254/
                                             #https://codereview.qt-project.org/#/c/149550/
                    ("do-not-spawn-console-qprocess-startdetached.patch", 1),#https://codereview.qt-project.org/#/c/162585/
                    ("fix-angle-mingw-5.6.2-20161027.diff", 1),
                    ("qdbus-manager-quit-5.7.patch", 1)  # https://phabricator.kde.org/D2545#69186
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
        if OsUtils.isWin():
            configure = os.path.join( self.sourceDir() ,"configure.bat" ).replace( "/", "\\" )
            if not os.path.exists(os.path.join(self.sourceDir(), ".gitignore")):  # force bootstrap of configure.exe
                with open(os.path.join(self.sourceDir(), ".gitignore"), "wt+") as bootstrap:
                    bootstrap.write("Force Bootstrap")
                if os.path.exists(os.path.join(self.sourceDir(), "configure.exe")):
                    os.remove(os.path.join(self.sourceDir(), "configure.exe"))
        elif OsUtils.isUnix():
            configure = os.path.join( self.sourceDir() ,"configure" )

        command = " %s -opensource  -confirm-license -prefix %s -platform %s " % ( configure, CraftStandardDirs.craftRoot(), self.platform )
        command += "-headerdir %s " % os.path.join(CraftStandardDirs.craftRoot(), "include", "qt5")
        command += "-qt-libpng "
        command += "-qt-libjpeg "
        # can we drop that in general?
        version = CraftVersion(self.subinfo.buildTarget)
        if version <= CraftVersion("5.6"):
            command += "-c++11 "
        if version >= CraftVersion("5.8"):
            command += "-mp "
        else:
            command += "-qt-pcre "
        if OsUtils.isWin():
            command += "-opengl dynamic "
            command += "-plugin-sql-odbc "
        if not OsUtils.isFreeBSD():
            command += "-ltcg "
        if self.buildType() == "RelWithDebInfo":
            command += "-force-debug-info "
        if self.buildType() == "Debug":
            command += "-debug "
        else:
            command += "-release "

        if not self.subinfo.options.buildStatic:
            command += "-I \"%s\" -L \"%s\" " % (os.path.join(CraftStandardDirs.craftRoot(), "include"), os.path.join(CraftStandardDirs.craftRoot(), "lib"))
            if self.subinfo.options.isActive("win32libs/openssl"):
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


        command += "-nomake examples "
        command += "-nomake tests "

        if (compiler.isMSVC() and compiler.isClang()) or OsUtils.isUnix() or self.supportsCCACHE:
            command += "-no-pch "

        print("command: ", command)
        return utils.system( command )

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
        if CraftVersion(self.subinfo.buildTarget) <  CraftVersion("5.8"):
            utils.putenv( "QMAKESPEC", os.path.join(self.sourceDir(), 'mkspecs', self.platform ))
        else:
            utils.putenv("QMAKESPEC", "")



