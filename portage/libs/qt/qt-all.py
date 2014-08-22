# -*- coding: utf-8 -*-

import utils
from utils import die
import os
import info
import portage
import emergePlatform
import compiler

from Package.QMakePackageBase import *

# ok we need something more here
# dbus-lib
# openssl-lib
# we can't use kde-root/include because we get conflicting includes then
# we have to make sure that the compiler picks up the correct ones!
# --> fetch the two libs above, unpack them into a separate folder

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = "[git]kde:qt|4.8"
        self.targets['4.8.4'] = "http://download.qt-project.org/archive/qt/4.8/4.8.4/qt-everywhere-opensource-src-4.8.4.tar.gz"
        self.targetInstSrc[ '4.8.4' ] = 'qt-everywhere-opensource-src-4.8.4'
        self.targetDigests['4.8.4'] = 'f5880f11c139d7d8d01ecb8d874535f7d9553198'
        self.targets['4.8.5'] = "http://download.qt-project.org/archive/qt/4.8/4.8.5/qt-everywhere-opensource-src-4.8.5.tar.gz"
        self.targetInstSrc[ '4.8.5' ] = 'qt-everywhere-opensource-src-4.8.5'
        self.targetDigests['4.8.5'] = '745f9ebf091696c0d5403ce691dc28c039d77b9e'
        self.targets['4.8.6'] = "http://download.qt-project.org/official_releases/qt/4.8/4.8.6/qt-everywhere-opensource-src-4.8.6.tar.gz"
        self.targetInstSrc[ '4.8.6' ] = 'qt-everywhere-opensource-src-4.8.6'
        self.targetDigests['4.8.6'] = 'ddf9c20ca8309a116e0466c42984238009525da6'

        self.patchToApply['4.8.4'] = [
            ('patches/4.8.4/out-of-source-build.patch', 1),
            ('patches/4.8.4/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8.4/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.4/Use-windows-path-for-pkgconfig-mkdir_p_asstring.patch', 1),
            ('patches/4.8.4/moc-boost-fix-bug-22829.diff', 1),
            ('patches/4.8.4/fix-defined-defined-and-do-not-include-inttypes-for-intel-compiler.patch', 1),
            ('patches/4.8.4/fix-Q_CORE_EXPORT_INLINE-for-intel-compiler.patch', 1),
        ]
        
        self.patchToApply['4.8.5'] = [
            ('patches/4.8.4/out-of-source-build.patch', 1),
            ('patches/4.8.4/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8.4/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.4/Use-windows-path-for-pkgconfig-mkdir_p_asstring.patch', 1),
            ('patches/4.8.5/fix-defined-defined-and-do-not-include-inttypes-for-intel-compiler.patch', 1),
            ('patches/4.8.4/fix-Q_CORE_EXPORT_INLINE-for-intel-compiler.patch', 1),
            ('patches/4.8.5/0001-fixed-build-with-new-mingw.patch', 1)
        ]

        self.patchToApply['4.8.6'] = [
            ('patches/4.8.4/out-of-source-build.patch', 1),
            ('patches/4.8.4/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8.4/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.4/Use-windows-path-for-pkgconfig-mkdir_p_asstring.patch', 1),
            ('patches/4.8.5/fix-defined-defined-and-do-not-include-inttypes-for-intel-compiler.patch', 1),
            ('patches/4.8.4/fix-Q_CORE_EXPORT_INLINE-for-intel-compiler.patch', 1),
        ]

        self.patchToApply['master'] = [
            ('patches/4.8.4/out-of-source-build.patch', 1),
            ('patches/4.8.4/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8.4/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.4/Use-windows-path-for-pkgconfig-mkdir_p_asstring.patch', 1),
            ('patches/4.8.5/fix-defined-defined-and-do-not-include-inttypes-for-intel-compiler.patch', 1),
            ('patches/4.8.4/fix-Q_CORE_EXPORT_INLINE-for-intel-compiler.patch', 1),
            ('patches/4.8.5/0001-fixed-build-with-new-mingw.patch', 1)
        ]
        

        self.shortDescription = "a cross-platform application framework"
        # If you change the default target here please do not forget to rename the portage file
        self.defaultTarget = '4.8.6'

        ## \todo this is prelimary  and may be changed
        self.options.package.packageName = 'qt'
        self.options.package.specialMode = True

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/dbus'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['binary/mysql-pkg'] = 'default'

class Package(QMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__(self)
        if not self.subinfo.options.useShortPathes \
                and self.compiler() == "mingw4" and len(self.rootdir) > 10:
            # mingw4 cannot compile qt if the command line arguments
            # exceed 8192 chars
            utils.warning('for mingw4, rootdir %s is too long for full path names.'
                ' Using short path names.' % self.rootdir)
            self.subinfo.options.useShortPathes = True
        # get instance of dbus and openssl package
        self.openssl = portage.getPackageInstance('win32libs', 'openssl')
        if self.subinfo.options.isActive("win32libs/dbus"):
            self.dbus = portage.getPackageInstance('win32libs', 'dbus')
        self.sqlite = portage.getPackageInstance('win32libs', 'sqlite')
        if self.subinfo.options.isActive("binary/mysql-pkg"):
            self.mysql_server = portage.getPackageInstance('binary', 'mysql-pkg')
        
    def unpack( self ):
        if not QMakePackageBase.unpack( self ): return False
        if self.subinfo.buildTarget != "master" and self.subinfo.buildTarget != "4.8.6":
            utils.copyFile( os.path.join( self.packageDir(), "configure.exe" ),
                    os.path.join( self.sourceDir(), "configure.exe" ) )
        return True

    def configure( self, unused1=None, unused2=""):
        self.enterBuildDir()
        self.setPathes()


        utils.putenv( "USERIN", "y")
        userin = "y"

        
        incdirs = " -I \"" + os.path.join( self.openssl.installDir(), "include" ) + "\""
        libdirs = " -L \"" + os.path.join( self.openssl.installDir(), "lib" ) + "\""
        if self.subinfo.options.isActive("win32libs/dbus"):
            incdirs += " -I \"" + os.path.join( self.dbus.installDir(), "include" ) + "\""
            libdirs += " -L \"" + os.path.join( self.dbus.installDir(), "lib" ) + "\""
        
        if os.getenv("INCLUDE"):
            utils.putenv( "INCLUDE", os.getenv( "INCLUDE" ) + ";" + os.path.join( self.sqlite.installDir(), "include" ))
        else:
            utils.putenv( "INCLUDE", os.path.join( self.sqlite.installDir(), "include" ))
        if os.getenv( "LIB" ):
            utils.putenv( "LIB", os.getenv( "LIB" ) + ";" + os.path.join( self.sqlite.installDir(), "lib" ))
        else:
            utils.putenv( "LIB", os.path.join( self.sqlite.installDir(), "lib" ))
        if self.isTargetBuild():
            incdirs += " -I \"" + os.path.join( self.wcecompat.installDir(), "include" ) + "\""
            libdirs += " -L \"" + os.path.join( self.wcecompat.installDir(), "lib" ) + "\""

        if self.subinfo.options.isActive("binary/mysql-pkg"):
            incdirs += " -I \"" + os.path.join( self.mysql_server.installDir(), "include" ) + "\""
            libdirs += " -L \"" + os.path.join( self.mysql_server.installDir(), "lib" ) + "\""
            libdirs += " -l libmysql "

        configure = os.path.join( self.sourceDir(), "configure.exe" ).replace( "/", "\\" )
        command = r"echo %s | %s -opensource -prefix %s -platform %s " % ( userin, configure, self.installDir(), self.platform )
        command += "-plugin-sql-odbc -system-sqlite "
        if self.subinfo.options.isActive("binary/mysql-pkg"):
            command += "-plugin-sql-mysql "
        command += "-qt-style-windowsxp -qt-style-windowsvista "
        command += "-qt-libpng -qt-libjpeg -qt-libtiff "

        # WebKit won't link properly with LTCG in a 32-bit MSVC environment
        if emergePlatform.buildArchitecture() == "x86" and compiler.isMSVC2008():
            command += "-no-ltcg "
        else:
            command += "-ltcg "

        # all builds
        command += "-no-phonon -no-qt3support "
        if self.subinfo.options.isActive("win32libs/dbus"):
            command += "-qdbus -dbus-linked "
        command += "-openssl-linked "
        command += "-no-fast -no-vcproj -no-dsp "
        command += "-nomake demos -nomake examples "
        command += "%s %s" % ( incdirs, libdirs )

        if self.buildType() == "Debug":
          command += " -debug "
        else:
          command += " -release "
        print("command: ", command)
        utils.system( command )
        return True

    def make(self, unused=''):
        if self.isTargetBuild():
            self.setupTargetToolchain()

        self.setPathes()

        QMakeBuildSystem.make(self)

        return True


    def install( self ):
        if self.isTargetBuild():
            # Configuring Qt for WinCE ignores the -prefix option,
            # so we have to do the job manually...

            # delete this because it is not working for windows
            utils.deleteFile( os.path.join( self.buildDir(), "plugin", "bearer", "qnmbearerd4.dll" ))
            utils.deleteFile( os.path.join( self.buildDir(), "plugin", "bearer", "qnmbearer4.dll" ))
            # syncqt expects qconfig.h to be in the install dir and fails if not
            utils.createDir( os.path.join( self.installDir(), "src", "corelib", "global") )
            utils.copyFile( os.path.join( self.buildDir(), "src", "corelib", "global", "qconfig.h" ), os.path.join( self.installDir(), "src", "corelib" , "global", "qconfig.h" ) )
            # headers need to be copied using syncqt because of the relative paths
            utils.prependPath(self.sourceDir(), "bin")
            command = os.path.join(self.sourceDir(), "bin", "syncqt.bat")
            command += " -base-dir \"" + self.sourceDir() + "\""
            command += " -outdir \"" + self.installDir() + "\""
            command += " -copy"
            command += " -quiet"
            utils.system( command )
            utils.copySrcDirToDestDir( os.path.join( self.buildDir(), "bin" ) , os.path.join( self.installDir(), "bin" ) )
            utils.copySrcDirToDestDir( os.path.join( self.buildDir(), "lib" ) , os.path.join( self.installDir(), "lib" ) )
            # the dlls must be copied to the bin dir too
            for file in os.listdir( os.path.join( self.installDir(), "lib" ) ):
                if file.endswith( ".dll" ):
                    utils.copyFile( os.path.join( self.installDir(), "lib" , file ), os.path.join( self.installDir(), "bin" , file ) )
            utils.copySrcDirToDestDir( os.path.join( self.buildDir(), "mkspecs" ) , os.path.join( self.installDir(), "mkspecs" ) )
            utils.copySrcDirToDestDir( os.path.join( self.buildDir(), "plugins" ) , os.path.join( self.installDir(), "plugins" ) )
            # create qt.conf
            utils.copyFile( os.path.join( self.packageDir(), "qt.conf" ), os.path.join( self.installDir(), "bin", "qt.conf" ) )
            return True

        if not QMakeBuildSystem.install(self):
            return False

        # Workaround QTBUG-12034
        utils.copySrcDirToDestDir( os.path.join( self.buildDir(), "plugins", "imageformats" ) ,
                                    os.path.join( self.installDir(), "bin", "imageformats" ) )

        # create qt.conf
        utils.copyFile( os.path.join( self.packageDir(), "qt.conf" ), os.path.join( self.installDir(), "bin", "qt.conf" ) )

        # install msvc debug files if available
        if compiler.isMSVC() or compiler.isIntel():
            srcdir = os.path.join( self.buildDir(), "lib" )
            destdir = os.path.join( self.installDir(), "lib" )

            filelist = os.listdir( srcdir )

            for file in filelist:
                if file.endswith( ".pdb" ):
                    utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ) )

        return True

if __name__ == '__main__':
    Package().execute()
