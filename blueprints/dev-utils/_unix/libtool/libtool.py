import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.4.6", "2.4.7"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/libtool/libtool-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libtool-{ver}"

        self.targetDigests["2.4.6"] = (
            ["7c87a8c2c8c0fc9cd5019e402bed4292462d00a718a7cd5f11218153bf28b26f"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2.4.7"] = (
            ["4f7f217f057ce655ff22559ad221a0fd8ef84ad1fc5fcb6990cecc333aa1635d"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.description = "GNU libtool is a generic library support script."
        self.patchLevel["2.4.6"] = 2
        self.defaultTarget = "2.4.7"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False

    def postInstall(self):
        return self.patchInstallPrefix(
            [(self.installDir() / x) for x in ["bin/libtool", "bin/libtoolize"]],
            self.subinfo.buildPrefix,
            CraftCore.standardDirs.craftRoot(),
        )
