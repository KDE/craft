import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.8.0']:
            self.targets[ver] = 'http://download.osgeo.org/proj/proj-%s.zip' % ver
            self.targetInstSrc[ver] = 'proj-' + ver
        self.patchToApply[ '4.8.0' ] = [ ( "proj-4.8.0-20120424.diff", 1 ) ]
        self.targetDigests['4.8.0'] = '15f51318b0314f107919b83bdab7b03f31193b75'
        self.shortDescription = "Projection library"
        self.defaultTarget = '4.8.0'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
