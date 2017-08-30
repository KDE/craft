import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.8.0", "3.8.1", "3.9.1"]:
            self.targets[ver] = f"https://www.cmake.org/files/v{ver[:3]}/cmake-{ver}-win{craftCompiler.bits}-{craftCompiler.architecture}.zip"
            self.targetInstSrc[ver] = f"cmake-{ver}-win{craftCompiler.bits}-{craftCompiler.architecture}"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "cmake")
            self.targetDigestUrls[ver] = (
            "https://cmake.org/files/v%s/cmake-%s-SHA-256.txt" % (ver[:3], ver), CraftHash.HashAlgorithm.SHA256)

        nightlyUrl = "https://cmake.org/files/dev/"
        for ver in utils.utilsCache.getNightlyVersionsFromUrl(nightlyUrl + "?C=M;O=D;F=0",
                                                              "\d.\d.\d\d\d\d\d\d\d\d-[0-9A-Za-z]{5,8}" + re.escape(
                                                                      "-win32-x86")):
            self.targets[ver] = f"{nightlyUrl}/cmake-{ver}.zip"
            self.targetInstSrc[ver] = f"cmake-{ver}"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "cmake")

        self.description = "CMake, the cross-platform, open-source build system."
        self.webpage = "http://www.cmake.org/"

        self.defaultTarget = "3.9.1"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"
        self.buildDependencies["gnuwin32/patch"] = "default"


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class CMakePackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        for name in ["cmake", "cmake-gui", "cmcldeps", "cpack", "ctest"]:
            if not utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", f"{name}.exe"),
                                    os.path.join(self.imageDir(), "dev-utils", "cmake", "bin", f"{name}.exe")):
                return False
        return True


class Package(VirtualIfSufficientVersion):
    def __init__(self):
        VirtualIfSufficientVersion.__init__(self, app="cmake", version="3.9.0", classA=CMakePackage)
