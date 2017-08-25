import info

from Package.AutoToolsPackageBase import *
from Package.PackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.3.10"]:
            self.targets[ver] = "ftp://ftp.gnutls.org/gcrypt/gnutls/v3.3/gnutls-%s.tar.xz" % ver
            self.targetInstSrc[ver] = "gnutls-%s" % ver
        self.patchToApply["3.3.10"] = ("0005-fix-strtok-conflict.mingw.patch", 1)
        self.targetDigests['3.3.10'] = 'b47af4ee116ba2099a24ff7a8e686079f80ec23a'
        self.description = "A library which provides a secure layer over a reliable transport layer"
        self.defaultTarget = "3.3.10"

    def setDependencies(self):
        self.runtimeDependencies["win32libs/gcrypt"] = "default"
        self.runtimeDependencies["win32libs/nettle"] = "default"
        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--with-zlib --enable-shared --disable-static --enable-cxx --enable-nls --disable-rpath --disable-gtk-doc --disable-guile --disable-libdane "
        self.subinfo.options.configure.cflags = "-I%s/usr/include " % utils.toMSysPath(
            CraftStandardDirs.msysDir())  # could cause problems but we need the autotools headers
        self.subinfo.options.configure.ldflags = "-L%s/usr/lib " % utils.toMSysPath(
            CraftStandardDirs.msysDir())  # could cause problems but we need the autotools libopt


if craftCompiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
