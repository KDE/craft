# -*- coding: utf-8 -*-
import info
import utils
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid
        # muon currently doesn't set the correct rpath for pkgconf
        # https://github.com/muon-build/muon/issues/135
        self.options.dynamic.setDefault("buildStatic", CraftCore.compiler.isMacOS)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/muon"] = None

    def setTargets(self):
        self.description = "package compiler and linker metadata toolkit"
        self.webpage = "https://github.com/pkgconf/pkgconf"
        self.releaseManagerId = 12753

        for ver in ["2.3.0", "2.4.3", "2.5.1"]:
            self.targets[ver] = f"https://distfiles.ariadne.space/pkgconf/pkgconf-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"pkgconf-{ver}"
        self.targets["2.9.91"] = "https://github.com/pkgconf/pkgconf/releases/download/pkgconf-2.9.91/pkgconf-2.9.91.tar.xz"
        self.targetInstSrc["2.9.91"] = "pkgconf-2.9.91"
        self.targetDigests["2.3.0"] = (["3a9080ac51d03615e7c1910a0a2a8df08424892b5f13b0628a204d3fcce0ea8b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.4.3"] = (["51203d99ed573fa7344bf07ca626f10c7cc094e0846ac4aa0023bd0c83c25a41"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.1"] = (["cd05c9589b9f86ecf044c10a2269822bc9eb001eced2582cfffd658b0a50c243"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.9.91"] = (["5a55b50bb7c6cab230c6f7f1835febb4c19a385b9cf3078fe0cf1c6dd49ca3b3"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.9.91"


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def _meson(self):
        # use muon im meson compat mode
        return [CraftCore.cache.findApplication("muon"), "meson"]

    def postInstall(self):
        return utils.createShim(self.installDir() / "bin/pkg-config", self.installDir() / f"bin/pkgconf{CraftCore.compiler.executableSuffix}")
