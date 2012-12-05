import os
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.4'] = "http://download.sourceforge.net/lcms/lcms2-2.4.tar.gz"
        self.targetInstSrc['2.4'] = "lcms2-2.4"
        self.patchToApply['2.4'] = ( 'lcms2-2.4-20121205.diff', 1 )
        self.targetDigests['2.4'] = '9944902864283af49e4e21a1ca456db4e04ea7c2'
        self.shortDescription = "A small-footprint, speed optimized color management engine"
        self.defaultTarget = '2.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_TESTS=ON -DBUILD_UTILS=OFF"


if __name__ == '__main__':
    Package().execute()
