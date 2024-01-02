import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/win-iconv/win-iconv.git"
        for ver in ["0.0.7", "0.0.8"]:
            self.targets[ver] = f"https://github.com/win-iconv/win-iconv/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"win-iconv-{ver}.tar.gz"
            self.targetInstSrc[ver] = "win-iconv-{ver}"

        self.targetDigests["0.0.8"] = (["23adea990a8303c6e69e32a64a30171efcb1b73824a1c2da1bbf576b0ae7c520"], CraftHash.HashAlgorithm.SHA256)

        self.description = "a character set conversion library binary compatible with GNU iconv"
        self.defaultTarget = "0.0.8"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.shelveAble = False
