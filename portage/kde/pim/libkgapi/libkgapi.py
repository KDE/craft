import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "KDE library for Google API"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/kwindowsystem'] = 'default'
        self.runtimeDependencies['kde/kcalcore'] = 'default'
        self.runtimeDependencies['kde/kcontacts'] = 'default'
        self.runtimeDependencies['libs/qtwebengine'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

