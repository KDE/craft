import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Configure Debug Categories"
        
    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependancies["libs/qtbase"] = "default"
        self.runtimeDependancies["frameworks/kcoreaddons"] = "default"
        self.runtimeDependancies["frameworks/ki18n"] = "default"
        self.runtimeDependancies["frameworks/kconfig"] = "default"
        self.runtimeDependancies["frameworks/kdbusaddons"] = "default"
        self.runtimeDependancies["frameworks/kcompetion"] = "default"
        self.runtimeDependancies["frameworks/kitemviews"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
