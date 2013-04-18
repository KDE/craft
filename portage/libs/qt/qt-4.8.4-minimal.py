# -*- coding: utf-8 -*-

import utils
from utils import die
import os
import info
import portage
import emergePlatform
import compiler

from Package.QMakePackageBase import *

# A more minimal qt specially for gpg4win

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['4.8.4']:
            self.svnTargets[ver] = "git://gitorious.org/qt/qt.git||v4.8.4"
        self.svnTargets['wince'] = "git://gitorious.org/qt/qt.git|4.7|235d1d687dcc2d21860cd753c9d67964c5270be2"
        self.patchToApply['4.8.4'] = [
            ('patches/4.7/out-of-source-build.patch', 1),
            ('patches/4.8/add-pdbs-on-msvc.diff', 1),
            ('patches/4.8/fix-debug-webkit-linkage-QTBUG-20556.patch', 0),
            ('patches/4.8.1/Use-windows-path-for-pkgconfig-mkdir_p_asstring.patch', 1),
            ('patches/4.8/moc-boost-fix-bug-22829.diff', 1)
        ]

        self.shortDescription = "a cross-platform application framework"
        # If you change the default target here please do not forget to rename the portage file
        self.defaultTarget = '4.8.4'

        ## \todo this is prelimary  and may be changed
        self.options.package.packageName = 'qt'
        self.options.package.specialMode = True

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.dependencies['win32libs/dbus'] = 'default'

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
        self.dbus = portage.getPackageInstance('win32libs', 'dbus')

    def configure( self, unused1=None, unused2=""):
        self.enterBuildDir()
        self.setPathes()
        os.environ[ "USERIN" ] = "y"
        userin = "y"

        incdirs = " -I \"" + os.path.join( self.dbus.installDir(), "include" ) + "\""
        libdirs = " -L \"" + os.path.join( self.dbus.installDir(), "lib" ) + "\""

        configure = os.path.join( self.sourceDir(), "configure.exe" ).replace( "/", "\\" )
        # Build options
        command = r"echo %s | %s -opensource -prefix %s -platform %s " % ( userin, configure, self.installDir(), self.platform )
        command += "-no-qt3support -no-multimedia -no-declarative -no-scripttools -no-webkit "
        command += "-qt-style-windowsxp -qt-style-windowsvista "
        command += "-qt-libpng -qt-libjpeg -qt-libtiff "
        command += "-no-phonon "
        command += "-qdbus -dbus-linked -no-openssl "
        command += "-no-fast -no-vcproj -no-dsp "
        command += "-nomake demos -nomake examples -nomake tools "
        command += "%s %s" % ( incdirs, libdirs )

        # WebKit won't link properly with LTCG in a 32-bit MSVC environment
        if emergePlatform.buildArchitecture() == "x86" and compiler.isMSVC2008():
            command += " -no-ltcg "
        else:
            command += " -ltcg "

        if self.buildType() == "Debug":
          command += " -debug "
        else:
          command += " -release "
        print("command: ", command)
        utils.system( command )
        return True

    def make(self, unused=''):
        self.setPathes()

        QMakeBuildSystem.make(self)

        return True


    def install( self ):
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
