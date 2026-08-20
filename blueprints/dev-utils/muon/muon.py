# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
from pathlib import Path

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
        self.runtimeDependencies["dev-utils/ninja"] = None

    def setTargets(self):
        self.description = "muon is an implementation of the meson build system in c99 with minimal dependencies"
        self.webpage = "https://muon.build/"
        self.releaseManagerId = 375420

        for ver in ["0.6.0"]:
            self.targets[ver] = f"https://muon.build/releases/v{ver}/muon-v{ver}.tar.gz"
            self.targetDigests[ver] = (["90a8428bc2178c59b9f7ddd1cb1cc6355f4df0c3ac023f7eefd159ae4f054024"], CraftHash.HashAlgorithm.SHA256)
            self.targetInstSrc[ver] = f"muon-v{ver}"

        self.defaultTarget = "0.6.0"


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def _meson(self):
        # use muon im meson compat mode
        return [self.buildDir() / "muon-bootstrap", "meson"]

    def configure(self, defines=""):
        env = self._env()
        env["CFLAGS"] += " -DBOOTSTRAP_NO_SAMU "
        with utils.ScopedEnv(env):
            return utils.system([f"{self.sourceDir()}/bootstrap{'.sh' if CraftCore.compiler.isUnix else '.bat'}", self.buildDir()], cwd=self.sourceDir()) and utils.system(
                [
                    f"{self.buildDir()}/muon-bootstrap",
                    "setup",
                    "-Dlibcurl=disabled",
                    "-Dlibpkgconf=disabled",
                    "-Dsamurai=disabled",
                    "-Dlibarchive=disabled",
                    "-Dmeson-docs=disabled",
                    "-Dman-pages=disabled",
                    f"-Dprefix={self.installPrefix()}",
                    self.buildDir(),
                ],
                cwd=self.sourceDir(),
            )

    def installPrefix(self) -> Path:
        if CraftCore.compiler.isWindows:
            # muon struggles with windows paths
            return Path(super().installPrefix().as_posix()[2:])
        return super().installPrefix()
