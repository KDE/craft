import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KDEgames Library"
        self.patchToApply['17.04.0'] = [("libkdegames-17.04.0-fix-compile-windows.diff", 1)]
        self.patchToApply['17.04.1'] = [("libkdegames-17.04.1-fix-compile-windows.diff", 1)]

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies["win32libs/libsndfile"] = "default"
        self.dependencies["win32libs/openal-soft"] = "default"
        self.buildDependencies["frameworks/kcoreaddons"] = "default"
        self.buildDependencies["frameworks/kconfig"] = "default"
        self.buildDependencies["frameworks/kwidgetsaddons"] = "default"
        self.buildDependencies["frameworks/kcodecs"] = "default"
        self.buildDependencies["frameworks/karchive"] = "default"
        self.buildDependencies["frameworks/kdbusaddons"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["frameworks/kguiaddons"] = "default"
        self.buildDependencies["frameworks/kitemviews"] = "default"
        self.buildDependencies["frameworks/kcompletion"] = "default"
        self.buildDependencies["frameworks/ktextwidgets"] = "default"
        self.buildDependencies["frameworks/kxmlgui"] = "default"
        self.buildDependencies["frameworks/kcrash"] = "default"
        self.buildDependencies["frameworks/kio"] = "default"
        self.buildDependencies["frameworks/kbookmarks"] = "default"
        self.buildDependencies["frameworks/kdnssd"] = "default"
        self.buildDependencies["frameworks/kdeclarative"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
