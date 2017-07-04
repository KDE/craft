import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Plugin based UI runtime used to write primary user interfaces"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies['frameworks/kactivities'] = "default"
        self.runtimeDependencies['frameworks/karchive'] = "default"
        self.runtimeDependencies['frameworks/kconfig'] = "default"
        self.runtimeDependencies['frameworks/kconfigwidgets'] = "default"
        self.runtimeDependencies['frameworks/kcoreaddons'] = "default"
        self.runtimeDependencies['frameworks/kdbusaddons'] = "default"
        self.runtimeDependencies['frameworks/kdeclarative'] = "default"
        self.runtimeDependencies['frameworks/kglobalaccel'] = "default"
        self.runtimeDependencies['frameworks/kguiaddons'] = "default"
        self.runtimeDependencies['frameworks/ki18n'] = "default"
        self.runtimeDependencies['frameworks/kiconthemes'] = "default"
        self.runtimeDependencies['frameworks/kio'] = "default"
        self.runtimeDependencies['frameworks/kservice'] = "default"
        self.runtimeDependencies['frameworks/kwindowsystem'] = "default"
        self.runtimeDependencies['frameworks/kxmlgui'] = "default"
        self.runtimeDependencies['frameworks/kdoctools'] = "default"
        self.runtimeDependencies['frameworks/kpackage'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

