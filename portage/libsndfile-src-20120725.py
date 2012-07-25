import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '1.0.24' ] = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.24.tar.gz'
        self.targetInstSrc[ '1.0.24' ] = 'libsndfile-1.0.24'
        self.patchToApply[ '1.0.24' ] = [( 'libsndfile-1.0.21-20101127.diff', 1 )]
        self.shortDescription = "a C library for reading and writing files containing sampled sound"
        self.targetDigests['1.0.24'] = 'ade2dad272b52f61bb58aca3a4004b28549ee0f8'
        self.defaultTarget = '1.0.24'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        self.dependencies[ 'win32libs-bin/libogg' ] = 'default'
        self.dependencies[ 'win32libs-bin/libvorbis' ] = 'default'

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

