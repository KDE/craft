import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Extra API to write KConfigModules"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["kde/kconfigwidgets"] = "default"
        self.dependencies["frameworks/kcoreaddons"] = "default"
        self.dependencies["kde/kiconthemes"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kitemviews"] = "default"
        self.dependencies["kde/kservice"] = "default"
        self.dependencies["kde/kxmlgui"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
