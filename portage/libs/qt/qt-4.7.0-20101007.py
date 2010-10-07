# -*- coding: utf-8 -*-
import base
import utils
from utils import die
import os
import info
import portage
import platform

from Package.QMakePackageBase import *

# ok we need something more here
# dbus-lib
# openssl-lib
# we can't use kde-root/include because we get conflicting includes then
# we have to make sure that the compiler picks up the correct ones!
# --> fetch the two libs above, unpack them into a separate folder

class subinfo(info.infoclass):
    def setTargets( self ):
        # the static version uses one of the stable versions
        self.svnTargets['static'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.5.2-patched|"
        # this is the upcoming 4.7 version with the KDE patches.
        self.svnTargets['master'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git"
        # this version contains the patches against the 4.5.3 release and is recommended for KDE 4.3.X
        self.svnTargets['4.5.3'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.5.3-patched|"
        # this branch contains all the patches and follows the 4.6-stable branch on qt.git - it updates daily
        self.svnTargets['4.6'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.6-stable-patched|"
        # those are the stable releases with the KDE patches applied on top
        self.svnTargets['4.6.0'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.6.0-patched|"
        self.svnTargets['4.6.1'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.6.1-patched|"
        self.svnTargets['4.6.2'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.6.2-patched|"
        self.svnTargets['4.6.3'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.6.3-patched|"
        self.svnTargets['4.7.0'] = "git://gitorious.org/+kde-developers/qt/kde-qt.git|4.7.0-patched|"
        self.svnTargets['4.7'] = "git://gitorious.org/qt/qt.git|4.7|"
        self.targetSrcSuffix['4.7'] = "4.7"
        self.patchToApply['4.6.3'] = ('qt-4.6.3.patch', 1)
        self.patchToApply['4.7'] = [
            ('qt-4.7.0-out-of-source-build.patch', 1),
            ('qt-4.7.0-webkit-fixes.patch', 1),
            ('qt-4.7.0-fix-build-with-QT_NO_SVG.patch', 1),
            ('qt-4.7.0-openssl-static-linking.patch', 1) ]
        if platform.isCrossCompilingEnabled():
            self.patchToApply['4.7'] += [
            ('qt-4.7.0-custom-flags-for-wince.patch', 1),
            ('qt-4.7.0-fix-build-uitools-for-wince.patch', 1),
            ('qt-4.7.0-exchange-malloc-against-dlmalloc-for-wince.patch', 1),
            ('qt-4.7.0-Override-new-in-qt-dlls-to-use-dlmalloc.patch',1)
            ]
        if platform.isCrossCompilingEnabled() or ( platform.buildArchitecture() == 'x64' and COMPILER == "mingw4" ) or COMPILER == "msvc2010":
            self.defaultTarget = '4.7'
        else:
            self.defaultTarget = '4.7.0'

        ## \todo this is prelimary  and may be changed 
        self.options.package.packageName = 'qt'
        self.options.package.specialMode = True

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        self.hardDependencies['win32libs-sources/dbus-src'] = 'default'
        if not platform.isCrossCompilingEnabled():
            self.hardDependencies['testing/mysql-pkg'] = 'default'
        else:
            self.hardDependencies['win32libs-sources/wcecompat-src'] = 'default'

class Package(PackageBase,GitSource, QMakeBuildSystem, KDEWinPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        GitSource.__init__(self)
        QMakeBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        # get instance of dbus and openssl package
        self.openssl = portage.getPackageInstance('win32libs-bin','openssl')
        self.dbus = portage.getPackageInstance('win32libs-sources','dbus-src')
        self.wcecompat = portage.getPackageInstance('win32libs-sources','wcecompat-src')
        if not platform.isCrossCompilingEnabled():
            self.mysql_server = portage.getPackageInstance('testing','mysql-pkg')

    def configure( self, unused1=None, unused2=""):
        self.enterBuildDir()
        self.setPathes()

        xplatform = ""
        if self.isTargetBuild():
            if self.buildPlatform() == "WM60":
                xplatform = "wincewm60professional-%s" % self.compiler()
            elif self.buildPlatform() == "WM65":
                xplatform = "wincewm65professional-%s" % self.compiler()
            elif self.buildPlatform() == "WM50":
                xplatform = "wincewm50pocket-%s" % self.compiler()
            else:
                exit( 1 )

        os.environ[ "USERIN" ] = "y"
        userin = "y"

        incdirs = " -I \"" + os.path.join( self.dbus.installDir(), "include" ) + "\""
        libdirs = " -L \"" + os.path.join( self.dbus.installDir(), "lib" ) + "\""
        incdirs += " -I \"" + os.path.join( self.openssl.installDir(), "include" ) + "\""
        libdirs += " -L \"" + os.path.join( self.openssl.installDir(), "lib" ) + "\""
        if self.isTargetBuild():
            libdirs += " -L \"" + os.path.join( self.wcecompat.installDir(), "lib" ) + "\""
        if not platform.isCrossCompilingEnabled():
            incdirs += " -I \"" + os.path.join( self.mysql_server.installDir(), "include" ) + "\""
            libdirs += " -L \"" + os.path.join( self.mysql_server.installDir(), "lib" ) + "\""
            libdirs += " -l libmysql "
        else:
            utils.copyFile( os.path.join( self.packageDir(), "qconfig-kde-wince.h" ),
                    os.path.join( self.sourceDir(), "src", "corelib" , "global", "qconfig-kde-wince.h" ) )
            utils.copyFile( os.path.join( self.packageDir(), "dlmalloc.c" ),
                    os.path.join( self.sourceDir(), "src", "corelib" , "global", "dlmalloc.c" ) )
            utils.copyFile( os.path.join( self.packageDir(), "dlmalloc.h" ),
                    os.path.join( self.sourceDir(), "src", "corelib" , "global", "dlmalloc.h" ) )
            utils.copyFile( os.path.join( self.packageDir(), "new.cpp" ),
                    os.path.join( self.sourceDir(), "src", "corelib" , "global", "new.cpp" ) )

        configure = os.path.join( self.sourceDir(), "configure.exe" ).replace( "/", "\\" )
        command = r"echo %s | %s -opensource -prefix %s -platform %s " % ( userin, configure, self.installDir(), self.platform )
        if platform.isCrossCompilingEnabled():
            if self.isTargetBuild():
                command += "-xplatform %s -qconfig kde-wince " % xplatform
                command += "-no-exceptions -no-stl -no-rtti "
            if self.isHostBuild():
                command += "-no-xmlpatterns -no-declarative -no-opengl "
            command += "-no-qt3support -no-multimedia -no-scripttools -no-accessibility -no-libmng -no-libtiff -no-gif -no-webkit "
            
        if not platform.isCrossCompilingEnabled():
            # non-cc builds only
            command += "-plugin-sql-odbc -plugin-sql-mysql "
            command += "-qt-style-windowsxp -qt-style-windowsvista "
            command += "-qt-libpng -qt-libjpeg -qt-libtiff "
        # all builds
        command += "-no-phonon "
        command += "-qdbus -dbus-linked -openssl-linked "
        command += "-fast -ltcg -no-vcproj -no-dsp "
        command += "-nomake demos -nomake examples "
        command += "%s %s" % ( incdirs, libdirs )

        if self.buildType() == "Debug":
          command += " -debug "
        else:
          command += " -release "
        print "command: ", command
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
            os.putenv( "PATH", os.path.join( self.sourceDir(), "bin" ) + ";" + os.getenv("PATH") )
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

        # create qt.conf 
        utils.copyFile( os.path.join( self.packageDir(), "qt.conf" ), os.path.join( self.installDir(), "bin", "qt.conf" ) )
        
        # install msvc debug files if available
        if self.buildType() == "Debug" and (self.compiler() == "msvc2005" or self.compiler() == "msvc2008" or self.compiler() == "msvc2010"):
            srcdir = os.path.join( self.buildDir(), "lib" )
            destdir = os.path.join( self.installDir(), "lib" )

            filelist = os.listdir( srcdir )
            
            for file in filelist:
                if file.endswith( ".pdb" ):
                    utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ) )
                
        return True

if __name__ == '__main__':
    Package().execute()
