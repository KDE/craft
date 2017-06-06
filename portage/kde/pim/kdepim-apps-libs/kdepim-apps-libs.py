import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KDEPIM-apps library"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["kdesupport/grantlee"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kiconthemes"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["frameworks/kservice"] = "default"
        self.buildDependencies["frameworks/kwidgetaddons"] = "default"
        
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/akonadi-contact"] = "default"
        self.buildDependencies["kde/kcontacts"] = "default"
        self.buildDependencies["kde/grantleetheme"] = "default"
        self.buildDependencies["kde/libkleo"] = "default"
        self.buildDependencies["kde/pimcommon"] = "default"
        self.buildDependencies["kdesupport/grantlee"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
