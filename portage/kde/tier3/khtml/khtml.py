import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KHTML APIs"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["win32libs/giflib"] = "default"
        self.dependencies["win32libs/jpeg"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/karchive"] = "default"
        self.dependencies["frameworks/kcodecs"] = "default"
        self.dependencies["frameworks/kglobalaccel"] = "default"
        self.dependencies["kde/kiconthemes"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["kde/kio"] = "default"
        self.dependencies["frameworks/kjs"] = "default"
        self.dependencies["kde/knotifications"] = "default"
        self.dependencies["kde/kparts"] = "default"
        self.dependencies["kde/ktextwidgets"] = "default"
        self.dependencies["kde/kwallet"] = "default"
        self.dependencies["frameworks/kwidgetsaddons"] = "default"
        self.dependencies["frameworks/sonnet"] = "default"
        self.dependencies["kde/kxmlgui"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
