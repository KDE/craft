import os
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['3.0'] = 'http://download.gna.org/getfem/stable/gmm-3.0.tar.gz'
        self.targetInstSrc['3.0'] = 'gmm-3.0'
        self.defaultTarget = '3.0'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        # header-only package
        self.createCombinedPackage = True

    def unpack( self ):
        if not CMakePackageBase.unpack(self):
            return False
        src = os.path.join( self.packageDir(), "CMakeLists.txt" )
        dst = os.path.join( self.sourceDir(), "CMakeLists.txt" )
        utils.copyFile( src, dst )
        return True

if __name__ == '__main__':
    Package().execute()
