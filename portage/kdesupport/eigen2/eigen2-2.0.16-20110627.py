import base
import utils
from utils import die
import sys
import info

# see http://eigen.tuxfamily.org/ for more informations

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        for ver in ['2.0.16']:
            # this is a repackaged version of eigen2 because the original tarball is not working
            self.targets[ ver ] = 'http://winkde.org/pub/kde/ports/win32/repository/other/eigen-2.0.16.tar.bz2'
            self.targetInstSrc[ ver ] = 'eigen-2.0.16'
        self.targetDigests['2.0.16'] = 'f36128efa6bde1ff72d7ea70f7e6ccc798d33641'
        self.defaultTarget = '2.0.16'

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
