# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= ~CraftCore.compiler.Platforms.MacOS

    def setTargets(self):
        for ver in ["1.15"]:
            self.targets[ver] = "https://ftp.gnu.org/pub/gnu/libiconv/libiconv-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libiconv-%s" % ver
        self.targetDigests["1.15"] = (["ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178"], CraftHash.HashAlgorithm.SHA256)

        self.description = "GNU internationalization (i18n)"
        self.defaultTarget = "1.15"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.shelveAble = False
