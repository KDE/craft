import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Grantlee Theme Editor"
        
    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kdoctools"] = "default"
        self.buildDependencies["frameworks/kxmlgui"] = "default"
        self.buildDependencies["frameworks/ktexteditor"] = "default"
        self.buildDependencies["frameworks/knewstuff"] = "default"
        self.buildDependencies["frameworks/karchive"] = "default"
        self.buildDependencies["frameworks/syntax-highlighting"] = "default"
        
            
        self.buildDependencies["kde/messagelib"] = "default"
        self.buildDependencies["kde/pimcommon"] = "default"
        self.buildDependencies["kde/grantleetheme"] = "default"
        self.buildDependencies["kde/akonadi-mime"] = "default"
        self.buildDependencies["kde/libkleo"] = "default"
        self.buildDependencies["kde/kimap"] = "default"
        self.buildDependencies["kde/kpimtextedit"] = "default"
        

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
