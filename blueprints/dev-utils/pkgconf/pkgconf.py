# -*- coding: utf-8 -*-
import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = ~CraftCore.compiler.Platforms.Android

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/automake"] = None

    def setTargets(self):
        self.description = "package compiler and linker metadata toolkit"
        for ver in ["2.3.0", "2.4.3"]:
            self.targets[ver] = f"https://distfiles.ariadne.space/pkgconf/pkgconf-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"pkgconf-{ver}"
        self.targetDigests["2.3.0"] = (["3a9080ac51d03615e7c1910a0a2a8df08424892b5f13b0628a204d3fcce0ea8b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.4.3"] = (["51203d99ed573fa7344bf07ca626f10c7cc094e0846ac4aa0023bd0c83c25a41"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.4.3"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # we could also use meson, but its not available during bootstrapping
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.autoreconf = False
        # the trailing slash is important
        # else pkgconf skipps the prefix
        self.subinfo.options.configure.args += [
            f"--with-system-includedir={CraftCore.standardDirs.craftRoot().as_posix()}/include/",
            f"--with-system-libdir={CraftCore.standardDirs.craftRoot().as_posix()}/lib/",
            f"--with-pkg-config-dir={CraftCore.standardDirs.craftRoot().as_posix()}/lib/pkgconfig/",
            f"--with-personality-dir={CraftCore.standardDirs.locations.data.as_posix()}/pkgconfig/personality.d/",
        ]
        if CraftCore.compiler.compiler.isMSVC:
            self.subinfo.options.configure.args += ["LIBS=-lAdvapi32"]

    def postInstall(self):
        return utils.createShim(self.installDir() / "bin/pkg-config", self.installDir() / f"bin/pkgconf{CraftCore.compiler.platform.executableSuffix}")
