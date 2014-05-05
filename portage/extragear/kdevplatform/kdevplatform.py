import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:kdevplatform|frameworks'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies[ 'kde/karchive' ] = 'default'
        self.dependencies[ 'kde/kcmutils' ] = 'default'
        self.dependencies[ 'kde/kconfig' ] = 'default'
        self.dependencies[ 'kde/kguiaddons' ] = 'default'
        self.dependencies[ 'kde/knewstuff' ] = 'default'
        self.dependencies[ 'kde/knotifyconfig' ] = 'default'
        self.dependencies[ 'kde/ki18n' ] = 'default'
        self.dependencies[ 'kde/kitemmodels' ] = 'default'
        self.dependencies[ 'kde/kitemviews' ] = 'default'
        self.dependencies[ 'kde/kxmlgui' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )

