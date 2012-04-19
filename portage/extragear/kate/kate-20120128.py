import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kate|KDE/4.8|'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.1/src/kate-4.8.0.tar.gz'
        for ver in [ '1', '2', '3', '4']:
            self.targets['4.8.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.' + ver + '/src/kate-4.8.' + ver + '.tar.xz'
            self.targetInstSrc['4.8.' + ver] = 'kate-4.8.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
