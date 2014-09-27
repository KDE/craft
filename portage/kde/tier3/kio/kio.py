import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Network transparent access to files and data"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["kde/karchive"] = "default"
        self.dependencies["kde/kbookmarks"] = "default"
        self.dependencies["kde/kcodecs"] = "default"
        self.dependencies["kde/kcompletion"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kconfigwidgets"] = "default"
        self.dependencies["frameworks/kcoreaddons"] = "default"
        self.dependencies["kde/kdbusaddons"] = "default"
        self.dependencies["kde/kdoctools"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kiconthemes"] = "default"
        self.dependencies["kde/kitemviews"] = "default"
        self.dependencies["kde/kjobwidgets"] = "default"
        self.dependencies["kde/knotifications"] = "default"
        self.dependencies["kde/kservice"] = "default"
        self.dependencies["kde/solid"] = "default"
        self.dependencies["frameworks/kwidgetsaddons"] = "default"
        self.dependencies["kde/kwindowsystem"] = "default"
        self.dependencies["kde/kxmlgui"] = "default"
        self.dependencies["kde/kwallet"] = "default"


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

