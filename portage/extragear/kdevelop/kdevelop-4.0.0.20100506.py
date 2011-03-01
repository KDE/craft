import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:kdevelop'
        for ver in [ '4.1.1' ]:
            self.targets[ ver ] = 'http://download.kde.org/download.php?url=stable/kdevelop/' + ver + '/src/kdevelop-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'kdevelop-' + ver
        self.patchToApply[ '4.1.1' ] = ( "kdevelop-4.1.1-20101228.diff", 1 )
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'virtual/kde-runtime' ] = 'default'
        self.dependencies[ 'virtual/kdeutils' ] = 'default'
        self.dependencies[ 'extragear/kate' ] = 'default'
        self.dependencies[ 'extragear/kdevplatform' ] = 'default'
        self.buildDependencies[ 'dev-util/zip' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
