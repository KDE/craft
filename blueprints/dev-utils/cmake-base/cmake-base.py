import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Windows | CraftCore.compiler.Platforms.MacOS | CraftCore.compiler.Platforms.Linux

    def setTargets(self):
        for ver in ["3.23.3"]:
            majorMinorStr = '.'.join(ver.split('.')[0:2])
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-windows-x86_64.zip"
                self.targetInstSrc[ver] = f"cmake-{ver}-windows-x86_64"
            elif CraftCore.compiler.isMacOS:
                self.targets[ver] = f"https://www.cmake.org/files/v{majorMinorStr}/cmake-{ver}-macos-universal.tar.gz"
                self.targetInstSrc[ver] = f"cmake-{ver}-macos-universal"
            elif CraftCore.compiler.isLinux:
                self.targets[ver] = f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-linux-x86_64.tar.gz"
                self.targetInstSrc[ver] = f"cmake-{ver}-linux-x86_64"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "cmake-base")
            self.targetDigestUrls[ver] = (f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-SHA-256.txt", CraftHash.HashAlgorithm.SHA256)

        self.description = "CMake, the cross-platform, open-source build system."
        self.webpage = "http://www.cmake.org/"

        self.patchLevel["3.13.2"] = 1

        self.defaultTarget = "3.23.3"

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
