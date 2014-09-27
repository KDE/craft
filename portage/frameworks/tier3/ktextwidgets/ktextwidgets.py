import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KTextWidgets provides widgets for displaying and editing text"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["frameworks/kcompletion"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kconfigwidgets"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kiconthemes"] = "default"
        self.dependencies["frameworks/kservice"] = "default"
        self.dependencies["frameworks/kwidgetsaddons"] = "default"
        self.dependencies["frameworks/kwindowsystem"] = "default"
        self.dependencies["frameworks/sonnet"] = "default"
        self.dependencies["frameworks/kconfigwidgets"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

