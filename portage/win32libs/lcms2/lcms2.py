import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.3', '2.4', '2.5']:
            self.targets[ ver ] = "http://download.sourceforge.net/lcms/lcms2-" + ver + ".tar.gz"
            self.targetInstSrc[ ver ] = "lcms2-" + ver
        self.patchToApply['2.3'] = [( 'lcms2-2.3-20120302.diff', 1 )]
        self.patchToApply['2.4'] = [( 'lcms2-2.4-20130124.diff', 1 )]
        self.patchToApply['2.5'] = [( 'lcms2-2.4-20130124.diff', 1 )]
        self.targetDigests['2.3'] = '67d5fabda2f5777ca8387766539b9c871d993133'
        self.targetDigests['2.4'] = '9944902864283af49e4e21a1ca456db4e04ea7c2'
        self.targetDigests['2.5'] = 'bab3470471fc7756c5fbe71be9a3c7d677d2ee7b'

        self.shortDescription = "A small-footprint, speed optimized color management engine"
        self.defaultTarget = '2.5'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_TESTS=ON -DBUILD_UTILS=OFF"


if __name__ == '__main__':
    Package().execute()
