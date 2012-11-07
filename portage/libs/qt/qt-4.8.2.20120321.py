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
        # the static version uses one of the stable versions
        self.svnTargets['static'] = "[git]kde:qt-kde|4.5.2-patched|"
        # this is the upcoming 4.7 version with the KDE patches.
        self.svnTargets['master'] = "[git]kde:qt-kde"
        # this version contains the patches against the 4.5.3 release and is recommended for KDE 4.3.X
        self.svnTargets['4.5.3'] = "[git]kde:qt-kde|4.5.3-patched|"
        # this branch contains all the patches and follows the 4.6-stable branch on qt.git - it updates daily
        self.svnTargets['4.6'] = "[git]kde:qt-kde|4.6-stable-patched|"
        # those are the stable releases with the KDE patches applied on top
        self.svnTargets['4.6.0'] = "[git]kde:qt-kde|4.6.0-patched|"
        self.svnTargets['4.6.1'] = "[git]kde:qt-kde|4.6.1-patched|"
        self.svnTargets['4.6.2'] = "[git]kde:qt-kde|4.6.2-patched|"
        self.svnTargets['4.6.3'] = "[git]kde:qt-kde|4.6.3-patched|"
        self.svnTargets['4.7.0'] = "[git]kde:qt-kde|4.7.0-patched|"
        self.svnTargets['4.7.1'] = "[git]kde:qt-kde|4.7.1-patched|"
        self.svnTargets['4.7.4'] = "[git]kde:qt|4.7-stable|v4.7.4"
        self.svnTargets['4.8.0'] = "[git]kde:qt|4.7-stable|v4.8.0"
        self.svnTargets['4.8.1'] = "[git]kde:qt|4.7-stable|v4.8.1"
        self.svnTargets['4.8.2'] = "[git]kde:qt|4.7-stable|v4.8.2"
        self.svnTargets['4.8.3'] = "[git]kde:qt|4.7-stable|v4.8.3"
        self.svnTargets['4.7'] = "git://gitorious.org/qt/qt.git|4.7|"
        self.svnTargets['wince'] = "git://gitorious.org/qt/qt.git|4.7|235d1d687dcc2d21860cd753c9d67964c5270be2"
        self.svnTargets['wince-4.7'] = self.svnTargets["4.7"]
        self.targetSrcSuffix['wince'] = "4.7"
        self.targetSrcSuffix['wince-4.7'] = "4.7"
        self.targetSrcSuffix['4.7'] = "4.7"
        self.targetSrcSuffix['4.7.4'] = "4.7.4"
        self.targetSrcSuffix['4.8.0'] = "4.8.0"
        self.targetSrcSuffix['4.8.1'] = "4.8.1"
        self.targetSrcSuffix['4.8.2'] = "4.8.2"
        self.targetSrcSuffix['4.8.3'] = "4.8.2"
        self.patchToApply['4.6.3'] = ('patches/4.6.3/fixed_export_macro_for_QtDbus.patch', 1)
        self.patchToApply['4.7'] = [
            ('patches/4.7/out-of-source-build.patch', 1),
            ('patches/4.7/webkit-fixes.patch', 1) ]
        self.patchToApply['4.7.1'] = [('patches/4.7.1/buildfix-for-mingw64.patch', 1)]
        self.patchToApply['4.7.4'] = [
            ('patches/4.7/out-of-source-build.patch', 1), 
            ('patches/4.7/add-pdbs-on-msvc.diff', 1) , 
            ("patches/4.7/detect-windows-8-as-windows-7.patch",1),
            ("patches/4.7.4/0001-fixed-error-generating-wrong-introspection-string-in.patch",1)
        ]
        self.patchToApply['4.8.0'] = [
            ('patches/4.7/out-of-source-build.patch', 1), 
            ('patches/4.8/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8/detect-windows-8-as-windows-7.patch', 1),
            ('patches/4.8/fixed-win32-detection.patch',1),
            ('patches/4.8/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.0/0001-Remove-implicit-const-char-QString-cast-from-QDBusSe.patch', 1)
        ]
        self.patchToApply['4.8.1'] = [
            ('patches/4.7/out-of-source-build.patch', 1),
            ('patches/4.8/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8/detect-windows-8-as-windows-7.patch', 1),
            ('patches/4.8/fixed-win32-detection.patch',1),
            ('patches/4.8/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.1/Use-windows-path-for-pkgconfig-mkdir_p_asstring.patch', 1)
        ]
        self.patchToApply['4.8.2'] = [
            ('patches/4.7/out-of-source-build.patch', 1),
            ('patches/4.8/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8/detect-windows-8-as-windows-7.patch', 1),
            ('patches/4.8/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.1/Use-windows-path-for-pkgconfig-mkdir_p_asstring.patch', 1),
            ('patches/4.8/moc-boost-fix-bug-22829.diff', 1)
        ]
        self.patchToApply['4.8.3'] = [
            ('patches/4.7/out-of-source-build.patch', 1),
            ('patches/4.8/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.1/Use-windows-path-for-pkgconfig-mkdir_p_asstring.patch', 1),
            ('patches/4.8/moc-boost-fix-bug-22829.diff', 1),
			('patches/4.8.3/fix-MinGW-w64-compilation.patch', 1)
        ]

        self.shortDescription = "a cross-platform application framework"
        # If you change the default target here please do not forget to rename the portage file
        self.defaultTarget = '4.8.3'

        ## \todo this is prelimary  and may be changed
        self.options.package.packageName = 'qt'
        self.options.package.specialMode = True

        # WinCE specific part
        winceVersionIndependentPatches = self.patchToApply['4.7'] + [
            ('patches/4.7/custom-flags-for-wince.patch', 1),
            ('patches/4.7/fix-build-uitools-for-wince.patch', 1),
            ('patches/4.7/exchange-malloc-against-dlmalloc-for-wince.patch', 1),
            ('patches/4.7/fix-endless-loop-in-qProcess-for-wince.patch', 1),
            ('patches/4.7/Replace-malloc-in-qimage.patch', 1),
            ('patches/4.7/Enable-Softkeyboard-wince.patch', 1),
            ('patches/4.7/comboboxes-wrong-direction_wince.patch', 1),
            ('patches/4.7/Add-gpgLogging.patch', 1),
            ('patches/4.7/allow-more-then-one-instance-of-a-wince-application.patch', 1),
            ('patches/4.7/Add-qCalloc-to-qmalloc.patch', 1),
            ('patches/4.7/Use-dlmalloc-in-QScript4.dll.patch', 1),
            ('patches/4.7/Use-dlmalloc-for-javascript-garbage-collector.patch', 1),
            ('patches/4.7/Use-dlmalloc-in-qpaintengine.patch', 1),
            ('patches/4.7/Use-qCalloc-instead-of-qt_wince_calloc-impl.patch', 1),
            ('patches/4.7/Use-qRealloc-instead-of-realloc-in-qimage.patch', 1),
            ('patches/4.7/fix-calloc.patch', 1)]
        self.patchToApply['wince']     =  winceVersionIndependentPatches + [
            ('patches/4.7/fix-qml-alignment.patch', 1), # Upstream in 4.7
            ('patches/4.7/Override-new-in-qt-dlls-to-use-dlmalloc.patch', 1),
            ('patches/4.7/Replace-qeventdispatcher.patch', 1),
            ('patches/4.7/fix-build-with-QT_NO_SVG.patch', 1),
            ('patches/4.7/fix-QSortFilterProxyModel.patch', 1),
            ('patches/4.7/Repaint-when-text-color-changes.patch', 1),
            ('patches/4.7/fix-map-to-global-calculations.patch', 1),
            ('patches/4.7/fix-widget-creation.patch', 1)]
        self.patchToApply['wince-4.7'] =  winceVersionIndependentPatches + [
            ('patches/4.7/Override-new-in-qt-dlls-for-4-7-branch.patch', 1),
            ('patches/4.7/Replace-qeventdispatcher-and-add-wcecompat-dep-for-4-7-branch.patch', 1),
            ('patches/4.7/fix-build-with-QT_NO_SVG-for-4-7-branch.patch', 1)]

        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = 'wince'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.dependencies['win32libs-bin/openssl'] = 'default'
        if EmergeBase().buildType() == "Debug":
            self.dependencies['win32libs-sources/dbus-src'] = 'default'
        else:
            self.dependencies['win32libs-bin/dbus'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['testing/mysql-pkg'] = 'default'
        else:
            self.dependencies['win32libs-sources/wcecompat-src'] = 'default'

class Package(PackageBase, GitSource, QMakeBuildSystem, KDEWinPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        if not self.subinfo.options.useShortPathes \
                and self.compiler() == "mingw4" and len(self.rootdir) > 10:
            # mingw4 cannot compile qt if the command line arguments
            # exceed 8192 chars
            utils.warning('for mingw4, rootdir %s is too long for full path names.'
                ' Using short path names.' % self.rootdir)
            self.subinfo.options.useShortPathes = True
        GitSource.__init__(self)
        QMakeBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        # get instance of dbus and openssl package
        self.openssl = portage.getPackageInstance('win32libs-bin', 'openssl')
        if self.buildType() == "Debug":
            self.dbus = portage.getPackageInstance('win32libs-sources', 'dbus-src')
        else:
            self.dbus = portage.getPackageInstance('win32libs-bin', 'dbus')
        if not emergePlatform.isCrossCompilingEnabled():
            self.mysql_server = portage.getPackageInstance('testing', 'mysql-pkg')
        else:
            self.wcecompat = portage.getPackageInstance('win32libs-sources', 'wcecompat-src')

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
            incdirs += " -I \"" + os.path.join( self.wcecompat.installDir(), "include" ) + "\""
            libdirs += " -L \"" + os.path.join( self.wcecompat.installDir(), "lib" ) + "\""
        if not emergePlatform.isCrossCompilingEnabled():
            incdirs += " -I \"" + os.path.join( self.mysql_server.installDir(), "include" ) + "\""
            libdirs += " -L \"" + os.path.join( self.mysql_server.installDir(), "lib" ) + "\""
            libdirs += " -l libmysql "
        else:
            utils.copyFile( os.path.join( self.packageDir(), "sources", "qconfig-kde-wince.h" ),
                    os.path.join( self.sourceDir(), "src", "corelib" , "global", "qconfig-kde-wince.h" ) )
            utils.copyFile( os.path.join( self.packageDir(), "sources", "new.cpp" ),
                    os.path.join( self.sourceDir(), "src", "corelib" , "global", "new.cpp" ) )
            utils.copyFile( os.path.join( self.packageDir(), "sources", "gpglogger_wince.cpp" ),
                    os.path.join( self.sourceDir(), "src", "corelib" , "global", "gpglogger_wince.cpp" ) )
            utils.copyFile( os.path.join( self.packageDir(), "sources", "gpglogger_wince.h" ),
                    os.path.join( self.sourceDir(), "src", "corelib" , "global", "gpglogger_wince.h" ) )

        configure = os.path.join( self.sourceDir(), "configure.exe" ).replace( "/", "\\" )
        command = r"echo %s | %s -opensource -prefix %s -platform %s " % ( userin, configure, self.installDir(), self.platform )
        if emergePlatform.isCrossCompilingEnabled():
            if self.isTargetBuild():
                command += "-xplatform %s -qconfig kde-wince " % xplatform
                command += "-no-exceptions -no-stl -no-rtti "
            if self.isHostBuild():
                command += "-no-xmlpatterns -no-declarative -no-opengl "
            command += "-no-qt3support -no-multimedia -no-scripttools -no-accessibility -no-libmng -no-libtiff -no-gif -no-webkit "

        if not emergePlatform.isCrossCompilingEnabled():
            # non-cc builds only
            command += "-plugin-sql-odbc -plugin-sql-mysql "
            command += "-qt-style-windowsxp -qt-style-windowsvista "
            command += "-qt-libpng -qt-libjpeg -qt-libtiff "

        # WebKit won't link properly with LTCG in a 32-bit MSVC environment
        if emergePlatform.buildArchitecture() == "x86" and compiler.isMSVC2008():
            command += "-no-ltcg "
        else:
            command += "-ltcg "

        # all builds
        command += "-no-phonon "
        command += "-qdbus -dbus-linked -openssl-linked "
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
        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008" or self.compiler() == "msvc2010":
            srcdir = os.path.join( self.buildDir(), "lib" )
            destdir = os.path.join( self.installDir(), "lib" )

            filelist = os.listdir( srcdir )

            for file in filelist:
                if file.endswith( ".pdb" ):
                    utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ) )

        return True

if __name__ == '__main__':
    Package().execute()
