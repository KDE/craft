import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # We need this as a host tool. Craft at this point isn't set up to produce both
        # host and target binaries, so on Android we have host tools in the docker image.
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.description = "GNU M4 is an implementation of the traditional Unix macro processor."
        self.webpage = "https://www.gnu.org/software/m4/"
        self.releaseManagerId = 1871

        for ver in ["1.4.19", "1.4.20", "1.4.21"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/m4/m4-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"m4-{ver}"

        self.targetDigests["1.4.19"] = (
            ["63aede5c6d33b6d9b13511cd0be2cac046f2e70fd0a07aa9573a04a82783af96"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.4.20"] = (
            ["e236ea3a1ccf5f6c270b1c4bb60726f371fa49459a8eaaebc90b216b328daf2b"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.4.21"] = (
            ["f25c6ab51548a73a75558742fb031e0625d6485fe5f9155949d6486a2408ab66"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.description = "GNU M4 is an implementation of the traditional Unix macro processor."
        self.releaseManagerId = 1871
        self.defaultTarget = "1.4.21"

    def setDependencies(self):
        self.buildDependencies["dev-utils/7zip"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        if CraftCore.compiler.isLinux and CraftCore.compiler.isClang():
            self.subinfo.options.configure.cflags += " --rtlib=compiler-rt"
            self.subinfo.options.configure.cxxflags += " --rtlib=compiler-rt"
