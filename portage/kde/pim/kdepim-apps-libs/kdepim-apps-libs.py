import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KDEPIM-apps library"
        
    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["kdesupport/grantlee"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = "default"
        self.runtimeDependencies["frameworks/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"
        self.runtimeDependencies["frameworks/kservice"] = "default"
        self.runtimeDependencies["frameworks/kwidgetaddons"] = "default"
        
        self.runtimeDependencies["kde/akonadi"] = "default"
        self.runtimeDependencies["kde/akonadi-contact"] = "default"
        self.runtimeDependencies["kde/kcontacts"] = "default"
        self.runtimeDependencies["kde/grantleetheme"] = "default"
        self.runtimeDependencies["kde/libkleo"] = "default"
        self.runtimeDependencies["kde/pimcommon"] = "default"
        self.runtimeDependencies["kdesupport/grantlee"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
