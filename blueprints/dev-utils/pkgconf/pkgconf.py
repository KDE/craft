# -*- coding: utf-8 -*-
import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid
        # we require a static build on Windows, as the symbols are not exported
        # self.options.dynamic.setDefault("buildStatic", True)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/automake"] = None

    def setTargets(self):
        self.description = "package compiler and linker metadata toolkit"
        for ver in ["2.3.0"]:
            self.targets[ver] = f"https://distfiles.ariadne.space/pkgconf/pkgconf-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"pkgconf-{ver}"
        self.targetDigests["2.3.0"] = (["3a9080ac51d03615e7c1910a0a2a8df08424892b5f13b0628a204d3fcce0ea8b"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.3.0"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # we could also use meson, but its not available during bootstrapping
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.autoreconf = False
        if CraftCore.compiler.isMSVC:
            self.subinfo.options.configure.args += ["LIBS=-lAdvapi32"]

    def postInstall(self):
        return utils.createShim(self.installDir() / "bin/pkg-config", self.installDir() / f"bin/pkgconf{CraftCore.compiler.executableSuffix}")
