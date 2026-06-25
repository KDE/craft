# -*- coding: utf-8 -*-
import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


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
            self.targetInstallPath[ver] = "dev-utils/bin"
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://muon.build/releases/v{ver}/muon-v{ver}-amd64-win.exe"
            elif CraftCore.compiler.isLinux:
                arch = "amd64"
                if CraftCore.compiler.architecture & CraftCore.compiler.Architecture.arm:
                    arch = "aarch64"
                self.targets[ver] = f"https://muon.build/releases/v{ver}/muon-v{ver}-{arch}-linux-small"
            else:
                self.targets[ver] = f"https://muon.build/releases/v{ver}/muon-v{ver}-universal-macos.zip"

        self.defaultTarget = "0.6.0"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        if CraftCore.compiler.isMacOS:
            return True
        versionedExe = self.subinfo.archiveName()[0]
        return utils.createShim(self.imageDir() / f"muon{CraftCore.compiler.executableSuffix}", self.imageDir() / f"/{versionedExe}")
