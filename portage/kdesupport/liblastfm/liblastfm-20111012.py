import os
import info
import shutil



class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = "git://github.com/TheOneRing/liblastfm.git"
        self.targetSrcSuffix['gitHEAD'] = "theo"
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


if __name__ == '__main__':
    Package().execute()
