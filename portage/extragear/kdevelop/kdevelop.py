import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:kdevelop'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'kde/kde-runtime' ] = 'default'
        self.dependencies[ 'kde/kate' ] = 'default'
        self.dependencies[ 'extragear/kdevplatform' ] = 'default'
        self.dependencies[ 'kde/libkomparediff2' ] = 'default'
        self.buildDependencies[ 'dev-util/zip' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )

