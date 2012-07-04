import os
import info
import shutil



class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = "git://github.com/TheOneRing/liblastfm.git"
        self.targetSrcSuffix['gitHEAD'] = "theo"
        self.targets['1.0.0'] = 'http://cdn.last.fm/client/liblastfm-1.0.0.tar.gz'
        self.targetDigests['1.0.0'] = '1947b1a6397ea188151572da33edc7699bf10164'
        self.targetInstSrc['1.0.0'] = 'liblastfm-1.0.0'
        self.shortDescription = "a C++/Qt4 library provided by Last.fm for use with their web services"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies[ 'libs/qt' ] = 'default'
        self.dependencies[ 'win32libs-bin/libfftw' ] = 'default'
        self.dependencies[ 'win32libs-bin/libsamplerate' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_FINGERPRINT=ON"


if __name__ == '__main__':
    Package().execute()
