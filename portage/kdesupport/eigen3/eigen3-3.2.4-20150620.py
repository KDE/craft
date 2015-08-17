import utils
from utils import die
import sys
import info

# see http://eigen.tuxfamily.org/ for more informations

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        for ver in ['3.2.5']:
            self.targets[ ver ] = 'http://bitbucket.org/eigen/eigen/get/3.2.5.tar.bz2'
            self.targetInstSrc[ ver ] = 'eigen-eigen-bdd17ee3b1b3'
        self.targetDigests['3.2.5'] = 'aa4667f0b134f5688c5dff5f03335d9a19aa9b3d'
        self.defaultTarget = '3.2.5'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_TESTS=OFF"
        # header-only package
        self.subinfo.options.package.withCompiler = False

if __name__ == '__main__':
    Package().execute()
