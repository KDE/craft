import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "PimCommon library"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"        
        self.buildDependencies["frameworks/kcompletion"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kcoreaddons"] = "default"
        self.buildDependencies["frameworks/kdbusaddons"] = "default"
        self.buildDependencies["frameworks/kiconthemes"] = "default"
        self.buildDependencies["frameworks/kitemmodels"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["frameworks/kjobwidgets"] = "default"
        self.buildDependencies["frameworks/knewstuff"] = "default"
        self.buildDependencies["frameworks/kservice"] = "default"
        self.buildDependencies["frameworks/kwallet"] = "default"
        self.buildDependencies["frameworks/kwidgetsaddons"] = "default"
        self.buildDependencies["frameworks/kwindowsystem"] = "default"
        self.buildDependencies["frameworks/kxmlgui"] = "default"
        self.dependencies['frameworks/kdesignerplugin'] = 'default'
        
        self.buildDependencies["kde/kmime"] = "default"
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/akonadi-contact"] = "default"
        self.buildDependencies["kde/akonadi-mime"] = "default"
        self.buildDependencies["kde/kpimtextedit"] = "default"
        self.buildDependencies["kde/kimap"] = "default"
        self.buildDependencies["kdesupport/grantlee"] = "default"
        self.dependencies['win32libs/libxslt'] = 'default'
        

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
