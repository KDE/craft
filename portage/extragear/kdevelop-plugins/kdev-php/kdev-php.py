import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '5.0' ] = '[git]kde:kdev-php|5.0'
        self.svnTargets[ '5.1' ] = '[git]kde:kdev-php|5.1'
        self.svnTargets[ 'master' ] = '[git]kde:kdev-php|master'
        self.defaultTarget = '5.1'

    def setDependencies( self ):
        self.runtimeDependencies[ 'extragear/kdevelop-pg-qt' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )

