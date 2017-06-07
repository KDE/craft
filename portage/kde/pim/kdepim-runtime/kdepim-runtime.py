import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "kdepim runtime"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/kdelibs4support"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/knotify"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["frameworks/kitemmodels"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"        
        self.buildDependencies["frameworks/kwindowsystem"] = "default"
        self.buildDependencies["frameworks/ktextwidgets"] = "default"
        
        self.buildDependencies["kde/kmime"] = "default"
        self.buildDependencies["kde/kdav"] = "default"
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/akonadi-contact"] = "default"
        self.buildDependencies["kde/akonadi-calendars"] = "default"
        self.buildDependencies["kde/akonadi-notes"] = "default"
        self.buildDependencies["kde/kcontacts"] = "default"
        self.buildDependencies["kde/kimap"] = "default"
        self.buildDependencies["kde/kcalutils"] = "default"
        self.buildDependencies["kde/kcalcore"] = "default"
        self.buildDependencies["kde/kmbox"] = "default"
        
        self.buildDependencies["kde/akonadi-mime"] = "default"
        self.buildDependencies["kde/libkgapi"] = "default"
        self.buildDependencies["kde/kpimtextedit"] = "default"
        self.buildDependencies["kdesupport/grantlee"] = "default"
        self.buildDependencies['win32libs/cyrus-sasl'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
