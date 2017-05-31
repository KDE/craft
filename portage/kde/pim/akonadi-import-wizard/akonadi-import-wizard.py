import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Akonadi-Import-Wizard Application"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kwallet"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kauth"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kdoctools"] = "default"        
        self.buildDependencies["frameworks/kdbusaddons"] = "default"        
        self.buildDependencies["frameworks/kcrash"] = "default"        
        self.buildDependencies["frameworks/kio"] = "default"        
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/libkdepim"] = "default"
        self.buildDependencies["kde/kcontacts"] = "default"
        self.buildDependencies["kde/kidentitymanagement"] = "default"
        self.buildDependencies["kde/kmailtransport"] = "default"
        self.buildDependencies["kde/mailcommon"] = "default"
        self.buildDependencies["kde/mailimporter"] = "default"
        self.buildDependencies["kde/pimcommon"] = "default"
        self.buildDependencies["kde/messagelib"] = "default"
        self.buildDependencies["kde/libkdepim"] = "default"


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
