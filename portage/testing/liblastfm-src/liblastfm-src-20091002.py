import os
import info
import shutil



class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://github.com/davidsansome/liblastfm.git"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['testing/libfftw'] = 'default'
        self.hardDependencies['testing/libsamplerate'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        #self.subinfo.options.configure.defines = "-DPNG_TESTS=OFF -DPNG_STATIC=OFF -DPNG_NO_STDIO=OFF"


if __name__ == '__main__':
    Package().execute()
