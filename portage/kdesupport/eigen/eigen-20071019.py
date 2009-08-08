import utils
import info

# http://download.tuxfamily.org/eigen/eigen-1.0.5.tar.gz
# see http://eigen.tuxfamily.org/ for more informations

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['1.0.5'] = 'http://download.tuxfamily.org/eigen/eigen-1.0.5.tar.gz'
        self.targetInstSrc['1.0.5'] = "eigen"
        self.defaultTarget = '1.0.5'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.withCompiler = False
        # header-only package

if __name__ == '__main__':
    Package().execute()
