import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '1.7.0' ] = 'http://download.savannah.nongnu.org/releases/openexr/openexr-1.7.0.tar.gz'
        self.targetInstSrc[ '1.7.0' ] = 'openexr-1.7.0'
        self.patchToApply[ '1.0.24' ] = [( 'openexr-1.7.0-20120804.diff', 1 )]
        self.targetDigests['1.7.0'] = '91d0d4e69f06de956ec7e0710fc58ec0d4c4dc2b'
        self.shortDescription = "a file format library for HDR images"
        self.defaultTarget = '1.7.0'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        self.dependencies[ 'win32libs/ilmbase' ] = 'default'

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )


