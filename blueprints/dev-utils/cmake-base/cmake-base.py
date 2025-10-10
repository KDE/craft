import os

import info
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = (
            CraftCore.compiler.Platforms.Windows | CraftCore.compiler.Platforms.MacOS | CraftCore.compiler.Platforms.Linux
        )

    def setTargets(self):
        for ver in ["3.23.3", "3.26.3", "3.30.0", "3.31.9", "4.1.2"]:
            majorMinorStr = ".".join(ver.split(".")[0:2])
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-windows-x86_64.zip"
                self.targetInstSrc[ver] = f"cmake-{ver}-windows-x86_64"
            elif CraftCore.compiler.isMacOS:
                self.targets[ver] = f"https://www.cmake.org/files/v{majorMinorStr}/cmake-{ver}-macos-universal.tar.gz"
                self.targetInstSrc[ver] = f"cmake-{ver}-macos-universal"
            elif CraftCore.compiler.isLinux:
                if CraftCore.compiler.hostArchitecture == CraftCore.compiler.Architecture.x86_64:
                    self.targets[ver] = f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-linux-x86_64.tar.gz"
                    self.targetInstSrc[ver] = f"cmake-{ver}-linux-x86_64"
                if CraftCore.compiler.hostArchitecture & CraftCore.compiler.Architecture.arm:
                    self.targets[ver] = f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-linux-aarch64.tar.gz"
                    self.targetInstSrc[ver] = f"cmake-{ver}-linux-aarch64"

            self.targetInstallPath[ver] = os.path.join("dev-utils", "cmake-base")
            self.targetDigestUrls[ver] = (
                f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-SHA-256.txt",
                CraftHash.HashAlgorithm.SHA256,
            )

        self.description = "CMake, the cross-platform, open-source build system."
        self.webpage = "http://www.cmake.org/"

        self.patchLevel["3.13.2"] = 1

        self.defaultTarget = "4.1.2"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
