import info
from CraftConfig import *


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:atcore|master'
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = "the KDE core of Atelier Printer Host"

    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qtserialport"] = "default"
        self.dependencies["frameworks/solid"] = "default"
        
from Package.CMakePackageBase import *


class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
