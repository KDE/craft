import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Libkdepim library"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"
        self.buildDependencies["frameworks/kcompletion"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kconfigaddons"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kiconthemes"] = "default"
        self.buildDependencies["frameworks/kitemviews"] = "default"
        self.buildDependencies["frameworks/kjobwidgets"] = "default"
        self.buildDependencies["frameworks/kwallet"] = "default"
        self.buildDependencies["frameworks/kwidgetaddons"] = "default"
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/akonadi-contacts"] = "default"
        self.buildDependencies["kde/kldap"] = "default"
        self.buildDependencies["kde/akonadi-search"] = "default"
        self.dependencies['frameworks/kdesignerplugin'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
