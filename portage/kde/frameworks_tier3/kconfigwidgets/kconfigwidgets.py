import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Extra widgets for easier configuration support"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/automoc"] = "default"
        self.dependencies["kde/kauth"] = "default"
        self.dependencies["kde/kcoreaddons"] = "default"
        self.dependencies["kde/kcodecs"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kdoctools"] = "default"
        self.dependencies["kde/kguiaddons"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kwidgetsaddons"] = "default"
        self.buildDependencies["dev-util/gettext-tools"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

