import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:kdevelop-pg-qt'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'extragear/kdevelop' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
