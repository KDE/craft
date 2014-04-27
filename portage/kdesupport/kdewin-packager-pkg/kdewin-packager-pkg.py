import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['HEAD'] = '[git]kde:kdewin-installer'
        self.defaultTarget = 'HEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.configure.defines = " -DBUILD_PACKAGER_ONLY=ON"

