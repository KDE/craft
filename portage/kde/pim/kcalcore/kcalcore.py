import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KCalcore library"
        self.patchToApply['17.04.1'] = [("kcalcore-fix-linking.diff", 1)]
        self.patchToApply['17.04.2'] = [("kcalcore-fix-linking.diff", 1)]

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["win32libs/libical"] = "default"
        self.runtimeDependencies["frameworks/kdelibs4support"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
