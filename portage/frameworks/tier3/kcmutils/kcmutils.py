import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Extra API to write KConfigModules"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kconfigwidgets"] = "default"
        self.dependencies["frameworks/kcoreaddons"] = "default"
        self.dependencies["frameworks/kiconthemes"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kitemviews"] = "default"
        self.dependencies["frameworks/kservice"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
