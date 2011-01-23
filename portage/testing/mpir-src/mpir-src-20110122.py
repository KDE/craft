import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'

    def setTargets( self ):
        self.targets['2.2.1'] = 'http://www.mpir.org/mpir-2.2.1.tar.bz2'
        self.targetInstSrc['2.2.1'] = "mpir-2.2.1"
        self.patchToApply['2.2.1'] = ('mpir-2.2.1-20110122.diff', 1)

        self.options.package.withCompiler = False
        self.shortDescription = "Library for arbitrary precision integer arithmetic derived from version 4.2.1 of gmp"
        self.defaultTarget = '2.2.1'

from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = "--enable-shared --disable-static --enable-gmpcompat"

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            self.subinfo = subinfo()
            VirtualPackageBase.__init__( self )

if __name__ == '__main__':
      Package().execute()
