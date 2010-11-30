import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '1.0.21' ] = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.21.tar.gz'
        self.targetInstSrc[ '1.0.21' ] = 'libsndfile-1.0.21'
        self.patchToApply[ '1.0.21' ] = ( 'libsndfile-1.0.21-20101127.diff', 1 )
        self.targetDigests[ '1.0.21' ] = '136845a8bb5679e033f8f53fb98ddeb5ee8f1d97'
        self.shortDescription = "a C library for reading and writing files containing sampled sound"
        self.defaultTarget = '1.0.21'

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
