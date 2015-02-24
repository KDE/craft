import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = '[git]kde:gpgmepp|master'
        self.defaultTarget = 'master'


    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/gpgme"] = "default"
        self.buildDependencies["win32libs/boost-headers"] = "default"
        self.buildDependencies["kdesupport/kdewin"] = "default"


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
