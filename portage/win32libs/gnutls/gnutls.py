import info

from Package.AutoToolsPackageBase import *
from Package.PackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ "3.3.1" ]:
            self.targets[ ver ]= "ftp://ftp.gnutls.org/gcrypt/gnutls/v3.3/gnutls-%s.tar.xz" % ver
            self.targetInstSrc[ ver ] = "gnutls-%s" % ver
        self.patchToApply[ "3.3.1" ] = ("0005-fix-strtok-conflict.mingw.patch", 1)
        self.targetDigests["3.3.1"] = "705846005198110a0d49aca21adafa34873d9092"
        self.shortDescription = "A library which provides a secure layer over a reliable transport layer"
        self.defaultTarget = "3.3.1"

    def setDependencies( self ):
        self.dependencies["win32libs/gcrypt"] = "default"
        self.dependencies["win32libs/nettle"] = "default"
        if compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"

class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = "--with-zlib --enable-shared --disable-static --enable-cxx --enable-nls --disable-rpath --disable-gtk-doc --disable-guile --disable-libdane "
        self.subinfo.options.configure.cflags = "-I%s/usr/include " % utils.toMSysPath( self.shell.msysdir ) #could cause problems but we need the autotools headers
        self.subinfo.options.configure.ldflags = "-L%s/usr/lib " % utils.toMSysPath( self.shell.msysdir ) #could cause problems but we need the autotools libopt

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            VirtualPackageBase.__init__( self )

