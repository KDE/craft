import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4.18", "1.4.19"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/m4/m4-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"m4-{ver}"

        self.targetDigests["1.4.18"] = (
            ["f2c1e86ca0a404ff281631bdc8377638992744b175afb806e25871a24a934e07"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.4.19"] = (
            ["63aede5c6d33b6d9b13511cd0be2cac046f2e70fd0a07aa9573a04a82783af96"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.description = "GNU M4 is an implementation of the traditional Unix macro processor."
        self.defaultTarget = "1.4.19"

        self.patchToApply["1.4.18"] = [
            ("m4-1.4.18-20190506.diff", 1),
            (
                "m4-1.4.18-glibc-change-work-around.patch",
                1,
            ),  # http://git.openembedded.org/openembedded-core/plain/meta/recipes-devtools/m4/m4/m4-1.4.18-glibc-change-work-around.patch
        ]
        self.patchLevel["1.4.18"] = 2

    def setDependencies(self):
        self.buildDependencies["dev-utils/7zip"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        if CraftCore.compiler.platform.isLinux and CraftCore.compiler.compiler.isClang:
            self.subinfo.options.configure.cflags += " --rtlib=compiler-rt"
            self.subinfo.options.configure.cxxflags += " --rtlib=compiler-rt"
