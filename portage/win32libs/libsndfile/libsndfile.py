import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '1.0.24' ] = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.24.tar.gz'
        self.targetInstSrc[ '1.0.24' ] = 'libsndfile-1.0.24'
        self.patchToApply[ '1.0.24' ] = [( 'libsndfile-1.0.24-20131003.diff', 1 )]
        self.targetDigests['1.0.24'] = 'ade2dad272b52f61bb58aca3a4004b28549ee0f8'

        self.shortDescription = "a C library for reading and writing files containing sampled sound"
        self.defaultTarget = '1.0.24'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        self.dependencies[ 'win32libs/libogg' ] = 'default'
        self.dependencies[ 'win32libs/libvorbis' ] = 'default'

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

