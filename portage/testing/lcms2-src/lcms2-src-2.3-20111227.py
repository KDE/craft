import os
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.3'] = "http://download.sourceforge.net/lcms/lcms2-2.3.tar.gz"
        self.targetInstSrc['2.3'] = "lcms2-2.3"
        self.patchToApply['2.3'] = ( 'lcms2-2.3-20111227.diff', 1 )
        self.targetDigests['2.3'] = '67d5fabda2f5777ca8387766539b9c871d993133'
        self.shortDescription = "A small-footprint, speed optimized color management engine"
        self.defaultTarget = '2.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
