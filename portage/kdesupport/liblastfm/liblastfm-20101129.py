import os
import info
import shutil



class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = "git://github.com/davidsansome/liblastfm.git"
        self.patchToApply[ 'gitHEAD' ] = ( "liblastfm-src-20101128.diff", 1 )
        self.svnTargets[ 'TheOneRing' ] = "git://github.com/TheOneRing/liblastfm.git"
        self.targetSrcSuffix['TheOneRing'] = "theo"
        self.defaultTarget = 'TheOneRing'

    def setDependencies( self ):
        self.dependencies[ 'libs/qt' ] = 'default'
        self.dependencies[ 'win32libs-bin/libfftw' ] = 'default'
        self.dependencies[ 'win32libs-bin/libsamplerate' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
