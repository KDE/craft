import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:kdevplatform'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'kde/kde-runtime' ] = 'default'
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
