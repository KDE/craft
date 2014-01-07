import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:kdevplatform'
        for ver in [ '4.1.1' ]:
            platformver = '1' + ver[ 1: ]
            self.targets[ ver ] = 'http://download.kde.org/download.php?url=stable/kdevelop/' + ver + '/src/kdevplatform-' + platformver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'kdevplatform-' + platformver
        self.patchToApply[ '4.1.1' ] = ( "kdevplatform-1.1.1-20101215.diff", 1 )
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'virtual/kde-runtime' ] = 'default'
        self.dependencies[ 'win32libs/boost' ] = 'default'
        self.dependencies[ 'kdesupport/qjson' ] = 'default'
        self.buildDependencies[ 'dev-util/gettext-tools' ] = 'default'
        self.buildDependencies[ 'dev-util/zip' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
