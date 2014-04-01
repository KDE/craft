# -*- coding: utf-8 -*-

import utils
from utils import die
import os
import info
import portage
import emergePlatform
import compiler

from Package.Qt5CorePackageBase import *

# there is a bug in qmake which results in install targets like
# V:${INSTALL_ROOT}\build\libs\qtbase\bin
# that is why I remove the first two character of installroot in Qt5CorePackageBase
# and why I set the prefix to the first 3 chars of KDEROOT
# its a ugly hack based on bugs but it works somehow

class subinfo(info.infoclass):
    def setTargets( self ):
        self.setupDefaultVersions(__file__)
        self.svnTargets['gitHEAD'] = '[git]git://gitorious.org/qt/%s.git|dev' % self.package
        self.svnTargets[self.defaultBranch()] = '[git]git://gitorious.org/qt/%s.git|%s' % ( self.package, self.defaultBranch())
        self.targets[self.defaultTag()] = 'http://download.qt-project.org/official_releases/qt/5.2/%s/submodules/%s-opensource-src-%s.zip' % ( self.defaultTag(), self.package, self.defaultTag())
        self.targetDigestUrls[self.defaultTag()] = 'http://download.qt-project.org/official_releases/qt/5.2/%s/submodules/%s-opensource-src-%s.zip.sha1' % (self.defaultTag(), self.package, self.defaultTag())
        self.targetInstSrc[self.defaultTag()] = '%s-opensource-src-%s' % ( self.package, self.defaultTag())

        self.patchToApply[ 'gitHEAD' ] = ("qtbase-20130714.patch" , 1)
        self.patchToApply[ self.defaultBranch() ] = ("qtbase-20130714.patch" , 1)
        self.patchToApply[ self.defaultTag() ] = ("qtbase-20130714.patch" , 1)
        
        self.shortDescription = "a cross-platform application framework"
        self.defaultTarget = self.defaultBranch()


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
        self.subinfo = subinfo()
        Qt5CorePackageBase.__init__(self)
        if not self.subinfo.options.useShortPathes \
                and compiler.isMinGW()  and len(self.rootdir) > 10:
            # mingw4 cannot compile qt if the command line arguments
            # exceed 8192 chars
            utils.warning('for mingw4, rootdir %s is too long for full path names.'
                ' Using short path names.' % self.rootdir)
            self.subinfo.options.useShortPathes = True
        
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

        configure = os.path.join( self.sourceDir() ,"configure.bat" ).replace( "/", "\\" )
        command = " %s -opensource  -confirm-license -prefix %s -platform %s " % ( configure, os.getenv("KDEROOT")[0:3], self.platform )
        command += "-plugin-sql-odbc "
        command += "-qt-style-windowsxp  -qt-style-windowsvista "
        command += "-qt-libpng "
        command += "-qt-libjpeg "
        command += "-qt-zlib "
        command += "-no-vcproj "
        command += "-nomake examples "
        command += "-c++11 "
        
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
          command += " -debug "
        else:
          command += " -release "
        print("command: ", command)
        utils.system( command )
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



if __name__ == '__main__':
    Package().execute()
