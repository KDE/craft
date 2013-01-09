import info

class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        self.buildDependencies[ 'dev-util/upx' ] = 'default'

    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]kde:automoc|no-qt|'
        self.defaultTarget = 'gitHEAD'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.version = "gitHEAD"

if __name__ == '__main__':
    Package().execute()
