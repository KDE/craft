import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Network transparent access to files and data"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["frameworks/karchive"] = "default"
        self.dependencies["frameworks/kbookmarks"] = "default"
        self.dependencies["frameworks/kcodecs"] = "default"
        self.dependencies["frameworks/kcompletion"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kconfigwidgets"] = "default"
        self.dependencies["frameworks/kcoreaddons"] = "default"
        self.dependencies["frameworks/kdbusaddons"] = "default"
        self.dependencies["frameworks/kdoctools"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kiconthemes"] = "default"
        self.dependencies["frameworks/kitemviews"] = "default"
        self.dependencies["frameworks/kjobwidgets"] = "default"
        self.dependencies["frameworks/knotifications"] = "default"
        self.dependencies["frameworks/kservice"] = "default"
        self.dependencies["frameworks/solid"] = "default"
        self.dependencies["frameworks/kwidgetsaddons"] = "default"
        self.dependencies["frameworks/kwindowsystem"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"
        self.dependencies["frameworks/kwallet"] = "default"


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

