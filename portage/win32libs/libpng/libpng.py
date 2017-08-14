import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.4.4', '1.2.43', '1.5.14', '1.5.28', '1.6.6', '1.6.27']:
            self.targets[ver] = 'http://downloads.sourceforge.net/libpng/libpng-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'libpng-' + ver
        self.targetDigests['1.4.4'] = '245490b22086a6aff8964b7d32383a17814d8ebf'
        self.targetDigests['1.5.14'] = '67f20d69564a4a50204cb924deab029f11ad2d3c'
        self.targetDigests['1.6.6'] = '609c355beef7c16ec85c4580eabd62efe75383af'
        self.targetDigests['1.5.28'] = (
            ['7dd9931dbdd43865055eeba52778ace6df5712b7f6f80f73c2b16b912c124a87'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.6.27'] = (
            ['c9d164ec247f426a525a7b89936694aefbc91fb7a50182b198898b8fc91174b4'], CraftHash.HashAlgorithm.SHA256)

        self.description = 'A library to display png images'
        self.defaultTarget = '1.5.28'

    def setDependencies(self):
        self.runtimeDependencies["win32libs/zlib"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DPNG_TESTS=OFF -DPNG_STATIC=OFF -DPNG_NO_STDIO=OFF"
        self.subinfo.options.package.packageName = 'libpng'
