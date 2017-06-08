import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "PIM Data Exporter"
        
    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/karchive"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = "default"
        self.runtimeDependencies["frameworks/kcrash"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/kitemviews"] = "default"
        self.runtimeDependencies["frameworks/knotifications"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/kdbusaddons"] = "default"
        self.runtimeDependencies["kde/akonadi"] = "default"
        self.runtimeDependencies["kde/kcontacts"] = "default"
        self.runtimeDependencies["kde/kidentitymanagement"] = "default"
        self.runtimeDependencies["kde/libkdepim"] = "default"
        self.runtimeDependencies["kde/mailcommon"] = "default"
        self.runtimeDependencies["kde/kmailtransport"] = "default"
        self.runtimeDependencies["kde/kmime"] = "default"
        self.runtimeDependencies["kde/pimcommon"] = "default"
        self.runtimeDependencies["kde/kpimtextedit"] = "default"



from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
