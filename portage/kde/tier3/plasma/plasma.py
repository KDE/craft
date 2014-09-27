import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( gitUrl="[git]kde:plasma-framework" )

        self.shortDescription = "Plugin based UI runtime used to write primary user interfaces"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['kde/kactivities'] = "default"
        self.dependencies['frameworks/karchive'] = "default"
        self.dependencies['frameworks/kconfig'] = "default"
        self.dependencies['frameworks/kconfigwidgets'] = "default"
        self.dependencies['frameworks/kcoreaddons'] = "default"
        self.dependencies['frameworks/kdbusaddons'] = "default"
        self.dependencies['kde/kdeclarative'] = "default"
        self.dependencies['frameworks/kglobalaccel'] = "default"
        self.dependencies['frameworks/kguiaddons'] = "default"
        self.dependencies['frameworks/ki18n'] = "default"
        self.dependencies['kde/kiconthemes'] = "default"
        self.dependencies['kde/kio'] = "default"
        self.dependencies['kde/kservice'] = "default"
        self.dependencies['frameworks/kwindowsystem'] = "default"
        self.dependencies['kde/kxmlgui'] = "default"
        self.dependencies['frameworks/kdoctools'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

