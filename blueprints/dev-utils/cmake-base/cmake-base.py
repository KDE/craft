import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Windows | CraftCore.compiler.Platforms.MacOS | CraftCore.compiler.Platforms.Linux
        self.options.dynamic.registerOption("checkForNightlies", False)

    def setTargets(self):
        for ver in ["3.13.0", "3.13.2", "3.16.3", "3.17.0", "3.17.2"]:
            majorMinorStr = '.'.join(ver.split('.')[0:2])
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://www.cmake.org/files/v{majorMinorStr}/cmake-{ver}-win{CraftCore.compiler.bits}-{CraftCore.compiler.architecture}.zip"
                self.targetInstSrc[ver] = f"cmake-{ver}-win{CraftCore.compiler.bits}-{CraftCore.compiler.architecture}"
            elif CraftCore.compiler.isMacOS:
                self.targets[ver] = f"https://www.cmake.org/files/v{majorMinorStr}/cmake-{ver}-Darwin-{CraftCore.compiler.gnuArchitecture}.tar.gz"
                self.targetInstSrc[ver] = f"cmake-{ver}-Darwin-{CraftCore.compiler.gnuArchitecture}"
            elif CraftCore.compiler.isLinux:
                self.targets[ver] = f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-Linux-x86_64.tar.gz"
                self.targetInstSrc[ver] = f"cmake-{ver}-Linux-x86_64"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "cmake-base")
            self.targetDigestUrls[ver] = (f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-SHA-256.txt", CraftHash.HashAlgorithm.SHA256)

        if CraftCore.compiler.isLinux and self.options.dynamic.checkForNightlies:
            suffix = 'zip' if CraftCore.compiler.isWindows else 'tar.gz'
            for ver in CraftCore.cache.getNightlyVersionsFromUrl("https://cmake.org/files/dev/?C=M;O=D;F=0",
                                                                f"\d.\d.\d\d\d\d\d\d\d\d-[0-9A-Za-z]{5,8}{re.escape('-win32-x86' if OsUtils.isWin() else '-Darwin-x86_64')}"):
                self.targets[ver] = f"{nightlyUrl}/cmake-{ver}.{suffix}"
                self.targetInstSrc[ver] = f"cmake-{ver}"
                self.targetInstallPath[ver] = os.path.join("dev-utils", "cmake-base")

        self.description = "CMake, the cross-platform, open-source build system."
        self.webpage = "http://www.cmake.org/"

        self.patchLevel["3.13.2"] = 1

        self.defaultTarget = "3.17.2"

from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
