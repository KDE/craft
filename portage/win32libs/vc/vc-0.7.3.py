import shutil
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.7.3'] = 'http://code.compeng.uni-frankfurt.de/attachments/download/174/Vc-0.7.3.tar.gz'
        self.targetDigests['0.7.3'] = 'aa41aeddac59abc60f292de8fdedbe70a4b49108'
        self.targetInstSrc['0.7.3'] = "Vc-0.7.3"
        self.shortDescription = 'Portable, zero-overhead SIMD library for C++'
        self.defaultTarget = '0.7.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

