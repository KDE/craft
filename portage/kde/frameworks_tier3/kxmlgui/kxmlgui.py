import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Framework for managing menu and toolbar actions"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/automoc"] = "default"
        self.dependencies["kde/kitemviews"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kglobalaccel"] = "default"
        self.dependencies["kde/kconfigwidgets"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kiconthemes"] = "default"
        self.dependencies["kde/ktextwidgets"] = "default"
        self.dependencies["kde/kwidgetsaddons"] = "default"
        self.dependencies["kde/attica"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

