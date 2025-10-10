# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.9.10", "1.2", "1.3", "1.4.1"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/libunistring/libunistring-{ver}.tar.xz"
            self.archiveNames[ver] = f"libunistring-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libunistring-{ver}"
        self.targetDigests["0.9.10"] = (["eb8fb2c3e4b6e2d336608377050892b54c3c983b646c561836550863003c05d7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.2"] = (["632bd65ed74a881ca8a0309a1001c428bd1cbd5cd7ddbf8cedcd2e65f4dcdc44"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.3"] = (["f245786c831d25150f3dfb4317cda1acc5e3f79a5da4ad073ddca58886569527"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.4.1"] = (["67d88430892527861903788868c77802a217b0959990f7449f2976126a307763"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.4.1"

        self.webpage = "https://www.gnu.org/software/libunistring/"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.runtimeDependencies["libs/iconv"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
