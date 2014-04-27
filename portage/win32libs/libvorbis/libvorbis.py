import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['1.3.1', '1.3.3']:
            self.targets[ ver ] = 'http://downloads.xiph.org/releases/vorbis/libvorbis-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'libvorbis-' + ver
        self.patchToApply['1.3.1'] = [( 'libvorbis-1.3.1-20100708.diff', 1 )]
        self.patchToApply['1.3.3'] = [( 'libvorbis-1.3.1-20100708.diff', 1 )]
        self.targetDigests['1.3.1'] = '0874dd08699240b868b22979da4c95ae6325006b'
        self.targetDigests['1.3.3'] = '8dae60349292ed76db0e490dc5ee51088a84518b'

        self.shortDescription = "reference implementation for the vorbis video file format"
        self.defaultTarget = '1.3.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/libogg'] = 'default'

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

