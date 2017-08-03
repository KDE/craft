# -*- coding: utf-8 -*-

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["6.0.0"] = "ftp://ftp.gmplib.org/pub/gmp-6.0.0/gmp-6.0.0.tar.bz2"
        self.targetDigests['6.0.0'] = 'c4976716a277b1d3b595171143f52f8c1a788284'
        self.targetInstSrc["6.0.0"] = "gmp-6.0.0"
        self.defaultTarget = "6.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.args = "--disable-static --enable-shared --enable-cxx "
        self.subinfo.options.useShadowBuild = False


if craftCompiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
