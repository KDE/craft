import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "IncidenceEditor library"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"
        self.buildDependencies["kde/kmime"] = "default"
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/akonadi-mime"] = "default"
        self.buildDependencies["kde/kldap"] = "default"
        self.buildDependencies["kde/calendarsupport"] = "default"
        self.buildDependencies["kde/eventviews"] = "default"
        self.buildDependencies["kde/kcalutils"] = "default"
        self.buildDependencies["kde/kcalcore"] = "default"
        self.buildDependencies["kde/kmailtransport"] = "default"
        

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
