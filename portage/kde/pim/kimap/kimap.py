import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Imap library"
        self.patchToApply['17.04.1'] = [("kimap-17.04.1-fix-windows.diff", 1)]
        
    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"
        self.runtimeDependencies["frameworks/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["kde/kmime"] = "default"
        self.dependencies['win32libs/cyrus-sasl'] = 'default'        


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
