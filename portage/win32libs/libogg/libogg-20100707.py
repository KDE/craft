import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['1.2.0', '1.3.0']:
            self.targets[ ver ] = 'http://downloads.xiph.org/releases/ogg/libogg-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'libogg-' + ver
        self.patchToApply['1.2.0'] = ( 'libogg-1.2.0-20100707.diff', 1 )
        self.patchToApply['1.3.0'] = ( 'libogg-1.2.0-20100707.diff', 1 )
        self.targetDigests['1.2.0'] = '135fb812282e08833295c91e005bd0258fff9098'
        self.targetDigests['1.3.0'] = 'a900af21b6d7db1c7aa74eb0c39589ed9db991b8'
        self.shortDescription = "reference implementation for the ogg audio file format"
        self.defaultTarget = '1.2.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
