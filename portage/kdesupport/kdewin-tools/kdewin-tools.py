import info
import compiler

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/libpng'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdewin'
        self.shortDescription = "kde supplementary tools package for win32"
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        # required for package generating because we build from gitHEAD by default
        self.subinfo.options.configure.defines = ''
        if compiler.isMinGW_W32():
            self.subinfo.options.configure.defines += ' -DMINGW_W32=ON '
        self.subinfo.options.configure.defines = '-DBUILD_BASE_LIB_WITH_QT=OFF -DBUILD_BASE_LIB=OFF -DBUILD_TOOLS=ON -DBUILD_QT_LIB=OFF'
        self.subinfo.options.package.version = '0.5.5'

