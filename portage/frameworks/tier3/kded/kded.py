import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Extensible deamon for providing system level services"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['frameworks/kinit'] = "default"
        self.dependencies['frameworks/kconfig'] = "default"
        self.dependencies['frameworks/kcoreaddons'] = "default"
        self.dependencies['frameworks/kcrash'] = "default"
        self.dependencies['frameworks/kdbusaddons'] = "default"
        self.dependencies['frameworks/kdoctools'] = "default"
        self.dependencies['frameworks/kservice'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

