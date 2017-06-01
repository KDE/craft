import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KAddressBook"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kdbusaddons"] = "default"
        self.buildDependencies["frameworks/kdoctools"] = "default"
        self.buildDependencies["frameworks/kcmutils"] = "default"
        self.buildDependencies["frameworks/kcrash"] = "default"
        self.buildDependencies["kde/libkleo"] = "default"
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/kontactinterface"] = "default"
        self.buildDependencies["kde/libkdepim"] = "default"
        self.buildDependencies["kde/pimcommon"] = "default"
        self.buildDependencies["kde/grantleetheme"] = "default"
        self.buildDependencies["kde/kdepim-apps-lib"] = "default"
        self.buildDependencies["kde/akonadi-search"] = "default"
        self.buildDependencies["win32libs/gpgme"] = "default"



from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
