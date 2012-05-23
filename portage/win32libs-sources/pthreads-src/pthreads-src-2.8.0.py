import utils
import os
import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.8.0'] = "ftp://sourceware.org/pub/pthreads-win32/pthreads-w32-2-8-0-release.tar.gz"
        self.targetInstSrc['2.8.0'] = 'pthreads-w32-2-8-0-release'
        self.patchToApply['2.8.0'] = [('pthreads-w32-2-8-0-release-20110729.diff', 1)]
        self.targetDigests['2.8.0'] = 'da8371cb20e8e238f96a1d0651212f154d84a9ac'
        self.shortDescription = 'a POSIX thread implementation for windows'
        self.defaultTarget = '2.8.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
from Package.VirtualPackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = " -DBUILD_TESTS=OFF"

if __name__ == '__main__':
    Package().execute()
