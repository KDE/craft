import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Calendar Support library"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"
        
        self.buildDependencies["kde/kmime"] = "default"
        self.buildDependencies["kde/akonadi-mime"] = "default"
        self.buildDependencies["kde/kcalutils"] = "default"
        self.buildDependencies["kde/kcalcore"] = "default"
        self.buildDependencies["kde/kidentitymanagement"] = "default"
        self.buildDependencies["kde/kholidays"] = "default"
        self.buildDependencies["kde/akonadi-calendar"] = "default"
        self.buildDependencies["kde/kimap"] = "default"
        

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
