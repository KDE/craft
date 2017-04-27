import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.patchToApply["5.33.0"] = [("0001-Fix-build-with-CMake-3.8.patch", 1)]

        self.shortDescription = "Plugin based UI runtime used to write primary user interfaces"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies['frameworks/kactivities'] = "default"
        self.dependencies['frameworks/karchive'] = "default"
        self.dependencies['frameworks/kconfig'] = "default"
        self.dependencies['frameworks/kconfigwidgets'] = "default"
        self.dependencies['frameworks/kcoreaddons'] = "default"
        self.dependencies['frameworks/kdbusaddons'] = "default"
        self.dependencies['frameworks/kdeclarative'] = "default"
        self.dependencies['frameworks/kglobalaccel'] = "default"
        self.dependencies['frameworks/kguiaddons'] = "default"
        self.dependencies['frameworks/ki18n'] = "default"
        self.dependencies['frameworks/kiconthemes'] = "default"
        self.dependencies['frameworks/kio'] = "default"
        self.dependencies['frameworks/kservice'] = "default"
        self.dependencies['frameworks/kwindowsystem'] = "default"
        self.dependencies['frameworks/kxmlgui'] = "default"
        self.dependencies['frameworks/kdoctools'] = "default"
        self.dependencies['frameworks/kpackage'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

