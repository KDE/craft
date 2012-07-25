import os
import info
import shutil



class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = "git://github.com/TheOneRing/liblastfm.git"
        self.targetSrcSuffix['gitHEAD'] = "theo"
        for ver in ['1.0.0','1.0.1']:
            self.targets[ver] = 'http://cdn.last.fm/client/liblastfm-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'liblastfm-%s' % ver
        self.targetDigests['1.0.0'] = '1947b1a6397ea188151572da33edc7699bf10164'
        self.targetDigests['1.0.1'] = '2d6adb2c265daa4b62bd9bf7fa8e45d2e29b9c37'
        
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
