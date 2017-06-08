import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "PIM Addons"
        
    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = "default"
        self.runtimeDependencies["frameworks/kdbusaddons"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/kdeclarative"] = "default"
        self.runtimeDependencies["kde/akonadi-notes"] = "default"
        self.runtimeDependencies["kde/kcalutils"] = "default"
        self.runtimeDependencies["kde/kpimtextedit"] = "default"
        self.runtimeDependencies["kde/kimap"] = "default"
        self.runtimeDependencies["kde/messagelib"] = "default"
        self.runtimeDependencies["kde/libkleo"] = "default"
        self.runtimeDependencies["kde/grantleetheme"] = "default"
        self.runtimeDependencies["kde/pimcommon"] = "default"
        self.runtimeDependencies["kde/incidenceeditor"] = "default"
        self.runtimeDependencies["kde/calendarsupport"] = "default"
        self.runtimeDependencies["kde/akonadi-calendar"] = "default"
        self.runtimeDependencies["kde/libgravatar"] = "default"
        self.runtimeDependencies["kde/kidentitymanagement"] = "default"
        self.runtimeDependencies["kde/libksieve"] = "default"
        self.runtimeDependencies["kde/kmailtransport"] = "default"
        self.runtimeDependencies["kde/akonadi-contact"] = "default"
        self.runtimeDependencies["kde/importwizard"] = "default"
        self.runtimeDependencies["kde/mailimporter"] = "default"
        

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
