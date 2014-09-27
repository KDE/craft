import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( gitUrl="[git]kde:plasma-framework" )

        self.shortDescription = "Plugin based UI runtime used to write primary user interfaces"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['kde/kactivities'] = "default"
        self.dependencies['kde/karchive'] = "default"
        self.dependencies['kde/kconfig'] = "default"
        self.dependencies['kde/kconfigwidgets'] = "default"
        self.dependencies['frameworks/kcoreaddons'] = "default"
        self.dependencies['kde/kdbusaddons'] = "default"
        self.dependencies['kde/kdeclarative'] = "default"
        self.dependencies['kde/kglobalaccel'] = "default"
        self.dependencies['frameworks/kguiaddons'] = "default"
        self.dependencies['kde/ki18n'] = "default"
        self.dependencies['kde/kiconthemes'] = "default"
        self.dependencies['kde/kio'] = "default"
        self.dependencies['kde/kservice'] = "default"
        self.dependencies['kde/kwindowsystem'] = "default"
        self.dependencies['kde/kxmlgui'] = "default"
        self.dependencies['kde/kdoctools'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

