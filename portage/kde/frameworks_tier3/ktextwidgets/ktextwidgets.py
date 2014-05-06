import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KTextWidgets provides widgets for displaying and editing text"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/automoc"] = "default"
        self.dependencies["kde/kcompletion"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kconfigwidgets"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kiconthemes"] = "default"
        self.dependencies["kde/kservice"] = "default"
        self.dependencies["kde/kwidgetsaddons"] = "default"
        self.dependencies["kde/kwindowsystem"] = "default"
        self.dependencies["kde/sonnet"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

