import info
from CraftConfig import *


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'master' ] = '[git]kde:atcore|master'
        self.defaultTarget = 'master'
        self.shortDescription = "the KDE core of Atelier Printer Host"

    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qtserialport"] = "default"
        self.dependencies["libs/qtcharts"] = "default"
        
from Package.CMakePackageBase import *


class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
