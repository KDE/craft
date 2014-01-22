import os
import info
import shutil



class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = "https://github.com/lastfm/liblastfm.git"
        for ver in ['1.0.0','1.0.1','1.0.2','1.0.3','1.0.8']:
            self.targets[ver] = 'https://github.com/lastfm/liblastfm/archive/%s.tar.gz' % ver
            self.archiveNames[ver] = "liblastfm-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'liblastfm-%s' % ver
        self.targetDigests['1.0.0'] = '1947b1a6397ea188151572da33edc7699bf10164'
        self.targetDigests['1.0.1'] = '2d6adb2c265daa4b62bd9bf7fa8e45d2e29b9c37'
        self.targetDigests['1.0.3'] = '4c6dc0eb2a32049fed72f8d713489edfad7b4eff'
        self.patchToApply['1.0.8'] = [ ('remove_atl_stuff.patch', 1) ]
        
        self.shortDescription = "a C++/Qt4 library provided by Last.fm for use with their web services"
        self.defaultTarget = '1.0.8'

    def setDependencies( self ):
        self.dependencies[ 'libs/qt' ] = 'default'
        self.dependencies[ 'win32libs/libfftw' ] = 'default'
        self.dependencies[ 'win32libs/libsamplerate' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DBUILD_FINGERPRINT=OFF -DBUILD_TESTS=OFF"


if __name__ == '__main__':
    Package().execute()
