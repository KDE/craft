import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Identity Management library"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kcoreaddons"] = "master"
        self.buildDependencies["frameworks/ktextwidgets"] = "master"
        self.buildDependencies["frameworks/kxmlgui"] = "master"
        self.buildDependencies["frameworks/kconfig"] = "master"
        self.buildDependencies["frameworks/kcodecs"] = "master"
        self.buildDependencies["frameworks/kiconthemes"] = "master"
        self.buildDependencies["frameworks/kio"] = "master"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
