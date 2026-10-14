# -*- coding: utf-8 -*-
# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
from pathlib import Path

import info
import shells
import utils
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = ~CraftCore.compiler.Platforms.Android

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/ninja"] = None

    def setTargets(self):
        self.description = "muon is an implementation of the meson build system in c99 with minimal dependencies"
        self.webpage = "https://muon.build/"
        self.releaseManagerId = 375420

        for ver in ["0.6.0", "0.7.0"]:
            self.targets[ver] = f"https://muon.build/releases/v{ver}/muon-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"muon-v{ver}"
        self.targetDigests["0.6.0"] = (["90a8428bc2178c59b9f7ddd1cb1cc6355f4df0c3ac023f7eefd159ae4f054024"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.7.0"] = (["573a3137e2a478e84e71dbbaf874623f7bc9848cf3367c948016ed284e8d637c"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.architecture.isArm64:
            self.patchToApply["0.7.0"] = [("muon-arm64.patch", 1)]

        self.defaultTarget = "0.7.0"


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
            if CraftCore.compiler.compiler.isMSVC:
                if not utils.system([f"{self.sourceDir()}/bootstrap.bat", self.buildDir()], cwd=self.sourceDir()):
                    return False
            else:
                bash = shells.BashShell()
                if not bash.execute(self.sourceDir(), f"{self.sourceDir()}/bootstrap.sh", bash.toNativePath(self.buildDir())):
                    return False
            return utils.system(
                [
                    f"{self.buildDir()}/muon-bootstrap{CraftCore.compiler.platform.executableSuffix}",
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
        if CraftCore.compiler.platform.isWindows:
            # muon struggles with windows paths
            return Path(super().installPrefix().as_posix()[2:])
        return super().installPrefix()
