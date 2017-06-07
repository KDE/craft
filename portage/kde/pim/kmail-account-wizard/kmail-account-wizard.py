import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KMail Account Wizard"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kcmutils"] = "default"        
        self.buildDependencies["frameworks/knotify"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kservice"] = "default"
        self.buildDependencies["frameworks/kdbusaddons"] = "default"
        self.buildDependencies["frameworks/kdoctools"] = "default"
        self.buildDependencies["frameworks/ktexteditor"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"
        self.buildDependencies["frameworks/kcrash"] = "default"                
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/kidentitymanagement"] = "default"
        self.buildDependencies["kde/kldap"] = "default"
        self.buildDependencies["kde/kmailtransport"] = "default"
        self.buildDependencies["kde/pimcommon"] = "default"
        self.buildDependencies["kde/libkdepim"] = "default"
        self.buildDependencies["kde/akonadi-mime"] = "default"
        self.buildDependencies["kde/kimap"] = "default"
        

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
