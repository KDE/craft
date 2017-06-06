import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Akregator"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kcrash"] = "default"
        self.buildDependencies["frameworks/kdoctools"] = "default"
        self.buildDependencies["frameworks/kcmutils"] = "default"
        self.buildDependencies["frameworks/knotifications"] = "default"
        self.buildDependencies["frameworks/kiconthemes"] = "default"
        self.buildDependencies["frameworks/kparts"] = "default"
        self.buildDependencies["frameworks/ktexteditor"] = "default"
        self.buildDependencies["frameworks/kxmlgui"] = "default"
        self.buildDependencies["frameworks/kdbusaddons"] = "default"
        
        self.buildDependencies["kde/grantleetheme"] = "default"
        self.buildDependencies["kde/kontactinterface"] = "default"
        self.buildDependencies["kde/libkdepim"] = "default"
        self.buildDependencies["kde/libkleo"] = "default"
        self.buildDependencies["kde/messagelib"] = "default"
        self.buildDependencies["kde/syndication"] = "default"
        self.buildDependencies["kde/akonadi-mime"] = "default"
        self.buildDependencies["kde/pimcommon"] = "default"



from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
