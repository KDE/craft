# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import stat

import info
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        ver = "latest"

        platform = ""
        compiler = ""
        arch = ""

        if CraftCore.compiler.isWindows:
            platform = "pc-windows"
            arch = "x86_64"
            compiler = "gnu" if CraftCore.compiler.isMinGW() else "msvc"
        elif CraftCore.compiler.isMacOS:
            platform = "apple"
            compiler = "darwin"
            arch = CraftCore.compiler.architecture.name.lower()
        elif CraftCore.compiler.isLinux:
            platform = "unknown-linux"
            compiler = "gnu"
            arch = CraftCore.compiler.appImageArchitecture
        elif CraftCore.compiler.isAndroid:
            archs = {
                CraftCompiler.Architecture.x86_32: "i686",
                CraftCompiler.Architecture.x86_64: "x86_64",
                # CraftCompiler.Architecture.arm32: "",
                CraftCompiler.Architecture.arm64: "aarch64",
            }
            platform = "linux"
            compiler = "android"
            arch = archs[CraftCore.compiler.architecture]

        self.targets[ver] = f"https://static.rust-lang.org/rustup/dist/{arch}-{platform}-{compiler}/rustup-init{CraftCore.compiler.executableSuffix}"
        self.targetInstallPath[ver] = "dev-utils/bin"

        self.defaultTarget = "latest"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False

        if CraftCore.compiler.isUnix:
            executable = self.installDir() / "rustup-init"
            CraftCore.log.info(f"Make {executable} executable")
            executable.chmod(executable.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        return True
