# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= ~CraftCore.compiler.Platforms.MacOS

    def setTargets(self):
        for ver in ["1.15", "1.18", "1.19.1"]:
            self.targets[ver] = "https://ftpmirror.gnu.org/libiconv/libiconv-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libiconv-%s" % ver
        self.targetDigests["1.15"] = (["ccf536620a45458d26ba83887a983b96827001e92a13847b45e4925cc8913178"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.19.1"] = (["9a06844846d664d7122161700c10a64480d7c7bcead3091925a785b38c91edab"], CraftHash.HashAlgorithm.SHA256)

        self.description = "GNU internationalization (i18n)"
        self.releaseManagerId = 10656

        self.defaultTarget = "1.19.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.shelveAble = False
