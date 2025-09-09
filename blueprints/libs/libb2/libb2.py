# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # On Android this links against libomp.so which is part of the toolchain but not properly deployed
        # resulting in APKs that don't start
        self.parent.package.categoryInfo.platforms = ~CraftCore.compiler.Platforms.Android

    def setTargets(self):
        for ver in ["0.98.1"]:
            self.targets[ver] = f"https://github.com/BLAKE2/libb2/releases/download/v{ver}/libb2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libb2-{ver}"
        self.targetDigests["0.98.1"] = (["53626fddce753c454a3fea581cbbc7fe9bbcf0bc70416d48fdbbf5d87ef6c72e"], CraftHash.HashAlgorithm.SHA256)

        self.description = "C library providing BLAKE2b, BLAKE2s, BLAKE2bp, BLAKE2sp"
        self.defaultTarget = "0.98.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.buildDependencies["dev-utils/pkgconf"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
        if CraftCore.compiler.platform.isWindows or CraftCore.compiler.platform.isAndroid:
            self.subinfo.options.configure.args += ["--disable-native"]
