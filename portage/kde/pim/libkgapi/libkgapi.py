import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "KDE library for Google API"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kwindowsystem'] = 'default'
        self.dependencies['kde/kcalcore'] = 'default'
        self.dependencies['kde/kcontacts'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

