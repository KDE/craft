# -*- coding: utf-8 -*-
import info
import utils
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None

    def setTargets(self):
        self.description = "package compiler and linker metadata toolkit"
        for ver in ["2.3.0"]:
            self.targets[ver] = f"https://github.com/pkgconf/pkgconf/archive/refs/tags/pkgconf-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"pkgconf-pkgconf-{ver}"
        self.targetDigests["2.3.0"] = (["0ee103cd390c3ee0e77a7a1c71dcb79a50a426fa2a648f6d07f2678c23adc5e3"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.3.0"


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        return utils.createShim(self.installDir() / "bin/pkg-config", self.installDir() / "bin/pkgconf")
