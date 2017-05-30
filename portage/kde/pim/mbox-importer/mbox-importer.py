import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Application for importing mbox files."
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kservices"] = "default"
        self.buildDependencies["frameworks/kcrash"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["kde/mailcommon"] = "default"
        self.buildDependencies["kde/pimcommon"] = "default"


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
