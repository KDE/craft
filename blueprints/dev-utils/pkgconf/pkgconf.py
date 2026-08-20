# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>

import os
import tempfile
from pathlib import Path

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
        for ver in ["3.0.3", "3.0.4", "3.0.5"]:
            self.targets[ver] = f"https://github.com/pkgconf/pkgconf/releases/download/pkgconf-{ver}/pkgconf-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"pkgconf-{ver}"
        self.targetDigests["2.3.0"] = (["3a9080ac51d03615e7c1910a0a2a8df08424892b5f13b0628a204d3fcce0ea8b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.4.3"] = (["51203d99ed573fa7344bf07ca626f10c7cc094e0846ac4aa0023bd0c83c25a41"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.1"] = (["cd05c9589b9f86ecf044c10a2269822bc9eb001eced2582cfffd658b0a50c243"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.0.3"] = (["aa033abb2b777ba4e66635495a931e53c49d86e4e4e38af68c0f76d666cbd8cf"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.0.5"] = (["3acd3a8a3cce65a8d620321855d92fb602e026cbe8e13ee36bdec58483b59ace"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.0.5"


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tmpPython = None
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.ldflags += "advapi32.lib"

    @property
    def _meson(self):
        # use muon im meson compat mode
        return [CraftCore.cache.findApplication("muon"), "meson"]

    def _env(self):
        env = super()._env()
        if CraftCore.compiler.isWindows:
            # help it find the system python
            if not self.tmpPython:
                self.tmpPython = tempfile.TemporaryDirectory()
                if not utils.createShim(Path(self.tmpPython.name) / f"python3{CraftCore.compiler.executableSuffix}", os.environ["CRAFT_PYTHON"]):
                    raise Exception("Failed to create shim")
            env["PATH"] = os.pathsep.join([os.environ["PATH"]] + [self.tmpPython.name])
        return env

    def installPrefix(self) -> Path:
        if CraftCore.compiler.isWindows:
            # muon struggles with windows paths
            return Path(super().installPrefix().as_posix()[2:])
        return super().installPrefix()

    def postInstall(self):
        return utils.createShim(self.installDir() / "bin/pkg-config", self.installDir() / f"bin/pkgconf{CraftCore.compiler.executableSuffix}")
