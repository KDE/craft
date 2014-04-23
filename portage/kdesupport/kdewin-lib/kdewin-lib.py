import info
import compiler

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.3.9'] = 'http://gitweb.kde.org/kdewin.git/snapshot/fc116df1dc204d8a06dc5c874a4cdecc335115ec.tar.gz'
        self.svnTargets['gitHEAD'] = '[git]kde:kdewin'
        self.shortDescription = "kde supplementary library for win32"
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        # required for package generating because we build from svnHEAD by default
        self.subinfo.options.package.version = '0.5.5'
        self.subinfo.options.configure.defines = '-DBUILD_BASE_LIB=ON -DBUILD_TOOLS=OFF -DBUILD_QT_LIB=OFF -DBUILD_BASE_LIB_WITH_QT=OFF '
        if compiler.isMinGW_W32():
          self.subinfo.options.configure.defines += ' -DMINGW_W32=ON '
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
