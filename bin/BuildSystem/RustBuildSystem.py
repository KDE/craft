# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from Utils.Arguments import Arguments


class RustBuildSystem(BuildSystemBase):
    def __init__(self, package: CraftPackageObject):
        BuildSystemBase.__init__(self, package, "pip")

        self.rustPackageName = self.package.name

    @property
    def __cargo(self):
        return CraftCore.cache.findApplication("cargo")

    def make(self):
        downloadDir = Path(CraftCore.standardDirs.downloadDir()) / "rust-packages" / self.package.path

        env = {
            "RUSTFLAGS": f"-L {CraftCore.standardDirs.craftRoot() / 'lib'}",
            "CARGO_HOME": downloadDir,
            "RUSTUP_HOME": CraftCore.standardDirs.craftRoot(),
        }

        with utils.ScopedEnv(env):
            command = Arguments(
                [
                    self.__cargo,
                    "build",
                    "--release",
                    "--target-dir",
                    self.buildDir(),
                    # TODO: this is an unstable feature and not yet available
                    # "--artifact-dir", self.installDir()
                ]
            )
            command += self.subinfo.options.make.args

            return utils.system(command, cwd=self.sourceDir())

    def install(self):
        return True

    def runTest(self):
        return False
