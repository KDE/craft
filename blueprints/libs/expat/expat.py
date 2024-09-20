import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        for ver in ["2.1.0", "2.2.10"]:
            self.targets[ver] = "https://github.com/libexpat/libexpat/releases/download/R_{tag}/expat-{ver}.tar.gz".format(tag=ver.replace(".", "_"), ver=ver)
            self.targetInstSrc[ver] = "expat-" + ver
        self.patchToApply["2.1.0"] = ("expat-2.1.0-20130311.diff", 1)
        self.targetDigests["2.1.0"] = "b08197d146930a5543a7b99e871cba3da614f6f0"
        self.targetDigests["2.2.10"] = (["bf42d1f52371d23684de36cc6d2f0f1acd02de264d1105bdc17792bbeb7e7ceb"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.2.10"] = [("expat-2.2.10-20210426.diff", 1), ("expat-2.1.0-20130311.diff", 1)]
        self.description = "XML parser library written in C"
        self.patchLevel["2.2.10"] = 5
        self.defaultTarget = "2.2.10"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # both examples and tests can be run here
        self.subinfo.options.configure.args = [
            "-DBUILD_tests=OFF",
            "-DBUILD_examples=OFF",
            "-DBUILD_tools=OFF",
            "-DEXPAT_BUILD_PKGCONFIG=ON",
            "-DEXPAT_BUILD_DOCS=OFF",
            "-DCMAKE_DEBUG_POSTFIX=",
        ]
        self.subinfo.options.configure.testDefine = ["-DBUILD_tests=ON", "-DBUILD_examples=ON"]
        self.subinfo.options.configure.args += [
            f"-DBUILD_tools={self.subinfo.options.dynamic.buildTools.asOnOff}",
            f"-DBUILD_shared={self.subinfo.options.dynamic.buildStatic.asOnOff}",
        ]  # available only from 2.1.0-beta3
