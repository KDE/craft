import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['win32libs/libbzip2'] = 'default'

    def setTargets( self ):
        self.svnTargets['master'] = '[git]kde:kdewin-installer'
        self.defaultTarget = 'master'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.make.supportsMultijob = False

    def configure(self):
        if self.buildTarget == 'amarokHEAD':
            self.subinfo.configure.defines = " -DBUILD_FOR_AMAROK=ON"
        return CMakePackageBase.configure(self)

