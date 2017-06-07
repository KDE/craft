import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KMail"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"        
        self.buildDependencies["frameworks/kcompletion"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kcrash"] = "default"
        self.buildDependencies["frameworks/kdbusaddons"] = "default"
        self.buildDependencies["frameworks/kdoctools"] = "default"
        self.buildDependencies["frameworks/kguiaddons"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["frameworks/kcmutils"] = "default"
        self.buildDependencies["frameworks/knotify"] = "default"
        self.buildDependencies["frameworks/kparts"] = "default"
        self.buildDependencies["frameworks/sonnet"] = "default"
        self.buildDependencies["frameworks/service"] = "default"
        self.buildDependencies["frameworks/ktextwidgets"] = "default"
        self.buildDependencies["frameworks/kwidgetsaddons"] = "default"
        self.buildDependencies["frameworks/kxmlgui"] = "default"

        
        self.buildDependencies["kde/kmime"] = "default"
        self.buildDependencies["kde/akonadi"] = "default"
        self.buildDependencies["kde/akonadi-contact"] = "default"
        self.buildDependencies["kde/akonadi-mime"] = "default"
        self.buildDependencies["kde/kpimtextedit"] = "default"
        self.buildDependencies["kde/kimap"] = "default"
        self.buildDependencies["kdesupport/grantlee"] = "default"
        self.buildDependencies["kde/kldap"] = "default"
        self.buildDependencies["kde/kcalcore"] = "default"
        self.buildDependencies["kde/kcalutils"] = "default"
        self.buildDependencies["kde/kidentitymanagement"] = "default"
        self.buildDependencies["kde/kmailtransport"] = "default"
        self.buildDependencies["kde/messagelib"] = "default"
        self.buildDependencies["kde/ktnef"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
