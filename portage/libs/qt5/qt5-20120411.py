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
        self.svnTargets['gitHEAD'] = "[git]git://gitorious.org/qt/qt5.git"
        #self.targetInstSrc['gitHEAD'] = 'qtbase/src'

        self.patchToApply['gitHEAD'] = [ ('patches/5/detect-windows-8-as-windows-7.patch', 1)  ]
        self.shortDescription = "a cross-platform application framework"
        # If you change the default target here please do not forget to rename the portage file
        self.defaultTarget = 'gitHEAD'

        ## \todo this is prelimary  and may be changed
        self.options.package.packageName = 'qt'
        self.options.package.specialMode = True


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.dependencies['win32libs-bin/openssl'] = 'default'
        self.dependencies['win32libs-bin/dbus'] = 'default'
        self.dependencies['testing/mysql-pkg'] = 'default'
        self.dependencies['win32libs-bin/jpeg'] = 'default'
        self.dependencies['win32libs-bin/libpng'] = 'default'

class Package(PackageBase, GitSource, QMakeBuildSystem, KDEWinPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        if not self.subinfo.options.useShortPathes \
                and compiler.isMinGW()  and len(self.rootdir) > 10:
            # mingw4 cannot compile qt if the command line arguments
            # exceed 8192 chars
            utils.warning('for mingw4, rootdir %s is too long for full path names.'
                ' Using short path names.' % self.rootdir)
            self.subinfo.options.useShortPathes = True
        GitSource.__init__(self)
        QMakeBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)


    def configure( self, unused1=None, unused2=""):
        #self.enterSourceDir()
        #utils.system( "perl init-repository -f" )
        
        self.enterBuildDir()
        self.setPathes()


        

        kderoot = os.getenv("KDEROOT")
        incdirs = " -I \"" + os.path.join( kderoot , "include" ) + "\""
        libdirs = " -L \"" + os.path.join( kderoot, "lib" ) + "\" "


        configure = os.path.join( self.sourceDir() ,"configure" ).replace( "/", "\\" )
        command = " %s -opensource  -confirm-license -prefix %s -platform %s " % ( configure, os.path.join(self.buildDir(),"qtbase"), self.platform )
        command += "-plugin-sql-odbc -plugin-sql-mysql "
        command += "-qt-style-windowsxp  -qt-style-windowsvista "
        command += "-qt-libpng "
        command += "-qt-libjpeg "
        command += "-l libmysql "



        # all builds
        #command += "-no-phonon "
        command += "-qdbus -dbus-linked "
        command += "-openssl-linked "
        command += "-qt-zlib "#with system-zlib it tries to ling with zdll.lib with msvc ...
        command += "-no-fast -no-vcproj -no-dsp "
        command += "-nomake demos -nomake examples -nomake tests -nomake docs  "
        command += "%s %s" % ( incdirs, libdirs )
       
        command += "-ltcg "

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
        utils.prependPath(os.path.join(self.buildDir(),"qtbase","bin"))
        utils.prependPath(os.path.join(self.sourceDir(),"qtbasebin"))
        utils.prependPath(os.path.join(self.sourceDir(),"qtrepotools","bin"))
        utils.prependPath(os.path.join(self.sourceDir(),"gnuwin32","bin"))
        # so that the mkspecs can be found, when -prefix is set
        utils.putenv( "QMAKEPATH", self.sourceDir() )
        # to be sure
        utils.putenv( "QMAKESPEC", os.path.join(self.sourceDir(),"qtbase", 'mkspecs', self.platform ))
          

if __name__ == '__main__':
    Package().execute()
