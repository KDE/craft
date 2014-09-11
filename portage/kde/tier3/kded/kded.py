import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Extensible deamon for providing system level services"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['kde/kinit'] = "default"
        self.dependencies['kde/kconfig'] = "default"
        self.dependencies['kde/kcoreaddons'] = "default"
        self.dependencies['kde/kcrash'] = "default"
        self.dependencies['kde/kdbusaddons'] = "default"
        self.dependencies['kde/kdoctools'] = "default"
        self.dependencies['kde/kservice'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

