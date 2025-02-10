# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
import utils
from CraftCore import CraftCore
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.runtimeDependencies["dev-utils/rustup-init"] = None


class Package(VirtualPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        version = "1.84.1"

        executable = CraftCore.cache.findApplication("rustup-init")

        with utils.ScopedEnv({"CARGO_HOME": self.installDir(), "RUSTUP_HOME": self.installDir()}):
            command = [executable, "--no-modify-path", "-y"]
            if version:
                command += [f"--default-toolchain={version}"]

            return utils.system(command)

    def internalPostInstall(self):
        super().internalPostInstall()
        return True
