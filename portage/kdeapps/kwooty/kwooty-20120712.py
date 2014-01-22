import info
import os

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = 'git://gitorious.org/kwooty/kwooty.git'
        for ver in ['0.8.4']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/kwooty/kwooty-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'kwooty-' + ver
        self.targetDigests['0.8.4'] = '574558ce934f8c53e1333c140f99b7dd7f467427'
        self.patchToApply['0.8.4'] = [("kwooty-exports.diff", 1)]
        self.shortDescription = "a nzb binary downloader for KDE4"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'kde/kde-runtime' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

