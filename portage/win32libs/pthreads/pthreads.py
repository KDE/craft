import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.8.0', '2.9.1']:
            ver2 = ver.replace('.', '-')
            self.targets[ver] = "ftp://sourceware.org/pub/pthreads-win32/pthreads-w32-" + ver2 + "-release.tar.gz"
            self.targetInstSrc[ver] = 'pthreads-w32-' + ver2 + '-release'

        self.patchToApply['2.8.0'] = [('pthreads-w32-2-8-0-release-20110729.diff', 1)]
        self.patchToApply['2.9.1'] = [('pthreads-w32-2-9-1-release-20130901.diff', 1)]
        self.targetDigests['2.8.0'] = 'da8371cb20e8e238f96a1d0651212f154d84a9ac'
        self.targetDigests['2.9.1'] = '24d40e89c2e66a765733e8c98d6f94500343da86'

        self.shortDescription = 'a POSIX thread implementation for windows'
        self.defaultTarget = '2.9.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
from Package.VirtualPackageBase import *

class PthreadsPackage(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = " -DBUILD_TESTS=OFF"


if compiler.isMSVC() or compiler.isIntel() or compiler.getMinGWVersion() == "4.4.7":
    class Package(PthreadsPackage):
        def __init__( self ):
            PthreadsPackage.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            self.subinfo = subinfo()
            VirtualPackageBase.__init__( self )

if __name__ == '__main__':
      Package().execute()
