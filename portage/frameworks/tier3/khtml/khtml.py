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
        self.dependencies["frameworks/kiconthemes"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/kjs"] = "default"
        self.dependencies["frameworks/knotifications"] = "default"
        self.dependencies["frameworks/kparts"] = "default"
        self.dependencies["frameworks/ktextwidgets"] = "default"
        self.dependencies["frameworks/kwallet"] = "default"
        self.dependencies["frameworks/kwidgetsaddons"] = "default"
        self.dependencies["frameworks/sonnet"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
