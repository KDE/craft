import info

from Package.AutoToolsPackageBase import *
from Package.PackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["2.7.1"]:
            self.targets[ ver ] = "http://www.lysator.liu.se/~nisse/archive/nettle-%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = "nettle-%s" % ver
            self.patchToApply[ ver ] = ("nettle-2.7.1-20140630.diff", 1)
        self.targetDigests['2.7.1'] = 'e7477df5f66e650c4c4738ec8e01c2efdb5d1211'

        self.shortDescription = "A low-level cryptographic library"
        self.defaultTarget = "2.7.1"

    def setDependencies( self ):
        if compiler.isMinGW():
            self.buildDependencies['dev-util/msys'] = 'default'
            self.dependencies['win32libs/libgmp'] = 'default'
            self.dependencies['win32libs/openssl'] = 'default'

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " --enable-shared  --enable-public-key --disable-documentation"

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            VirtualPackageBase.__init__( self )

