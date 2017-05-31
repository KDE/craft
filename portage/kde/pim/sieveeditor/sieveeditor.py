import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KDE Sieve Editor"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kdbusaddons"] = "default"
        self.buildDependencies["frameworks/kwallet"] = "default"
        self.buildDependencies["frameworks/kbookmarks"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kiconthemes"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["kde/kmime"] = "default"
        self.buildDependencies["kde/kpimtextedit"] = "default"
        self.buildDependencies["kde/kmailtransport"] = "default"
        self.buildDependencies["kde/libksieve"] = "default"
        self.buildDependencies["kde/kimap"] = "default"


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
