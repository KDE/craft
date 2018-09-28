import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.8.0", "3.8.1", "3.9.1", "3.10.2", "3.10.3", "3.11.0", "3.11.1", "3.11.3", "3.12.0", "3.12.2"]:
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
            self.targetInstallPath[ver] = os.path.join("dev-utils", "cmake")
            self.targetDigestUrls[ver] = (f"https://cmake.org/files/v{majorMinorStr}/cmake-{ver}-SHA-256.txt", CraftHash.HashAlgorithm.SHA256)

        if CraftCore.compiler.isLinux and self.options.dynamic.checkForNightlies:
            suffix = 'zip' if CraftCore.compiler.isWindows else 'tar.gz'
            for ver in CraftCore.cache.getNightlyVersionsFromUrl("https://cmake.org/files/dev/?C=M;O=D;F=0",
                                                                f"\d.\d.\d\d\d\d\d\d\d\d-[0-9A-Za-z]{5,8}{re.escape('-win32-x86' if OsUtils.isWin() else '-Darwin-x86_64')}"):
                self.targets[ver] = f"{nightlyUrl}/cmake-{ver}.{suffix}"
                self.targetInstSrc[ver] = f"cmake-{ver}"
                self.targetInstallPath[ver] = os.path.join("dev-utils", "cmake")

        self.description = "CMake, the cross-platform, open-source build system."
        self.webpage = "http://www.cmake.org/"

        self.defaultTarget = "3.12.2"


    def setDependencies(self):
        self.buildDependencies["dev-utils/ninja"] = None


    def registerOptions(self):
        self.options.dynamic.registerOption("checkForNightlies", False)


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        binaryPath = os.path.join(self.imageDir(), "dev-utils", "cmake", "bin")
        if OsUtils.isMac():
            binaryPath = os.path.join(self.imageDir(), "dev-utils", "cmake", "CMake.app", "Contents", "bin")

        for name in ["cmake", "cmake-gui", "cmcldeps", "cpack", "ctest"]:
            sourceBinary = os.path.join(binaryPath, f"{name}{CraftCore.compiler.executableSuffix}")
            targetBinary = os.path.join(self.imageDir(), "dev-utils", "bin", f"{name}{CraftCore.compiler.executableSuffix}")

            if os.path.exists(sourceBinary):
                if not utils.createShim(targetBinary, sourceBinary):
                    return False
        return True

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
