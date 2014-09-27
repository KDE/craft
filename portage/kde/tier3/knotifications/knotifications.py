import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "TODO"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["kde/kwindowsystem"] = "default"
        self.dependencies["kde/kservice"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kiconthemes"] = "default"
        self.dependencies["kde/kcodecs"] = "default"
        self.dependencies["frameworks/kcoreaddons"] = "default"
        self.dependencies["qt-libs/phonon"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

