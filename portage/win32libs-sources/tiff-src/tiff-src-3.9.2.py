import os
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.9.2'] = "ftp://ftp.remotesensing.org/pub/libtiff/tiff-3.9.2.tar.gz"
        self.targetInstSrc['3.9.2'] = "tiff-3.9.2"
        self.patchToApply['3.9.2'] = ( 'tiff-3.9.2-20100418.diff', 1 )
        self.targetDigests['3.9.2'] = '5c054d31e350e53102221b7760c3700cf70b4327'
        self.defaultTarget = '3.9.2'

    def setDependencies( self ):
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        # both examples and tests can be run here
        self.subinfo.options.configure.defines = "-DBUILD_TESTS=OFF -DBUILD_SAMPLES=ON -DBUILD_TOOLS=OFF"

if __name__ == '__main__':
    Package().execute()
