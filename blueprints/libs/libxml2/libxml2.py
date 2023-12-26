import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.10.3"]:
            self.targets[ver] = f"https://download.gnome.org/sources/libxml2/2.10/libxml2-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libxml2-{ver}"
        self.targetDigests["2.10.3"] = (["5d2cc3d78bec3dbe212a9d7fa629ada25a7da928af432c93060ff5c17ee28a9c"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.10.3"] = [
            ("libxml2-2.10.3-20221105.diff", 1),
            ("libxml2-2.10.3-20221114.diff", 1),
            ("libxml2-android-ecm-toolchain-workaround.diff", 1),
        ]
        self.patchLevel["2.10.3"] = 3

        self.description = "XML C parser and toolkit (runtime and applications)"
        self.defaultTarget = "2.10.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/icu"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += [
            "-DLIBXML2_WITH_PYTHON=OFF",
            f"-DLIBXML2_WITH_ICU={'ON' if self.subinfo.options.isActive('libs/icu') else 'OFF'}",
            f"-DLIBXML2_WITH_LZMA={'ON' if self.subinfo.options.isActive('libs/liblzma') else 'OFF'}",
        ]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DLIBXML2_WITH_ICONV=OFF", "-DLIBXML2_WITH_PROGRAMS=OFF", "-DLIBXML2_WITH_TESTS=OFF"]
