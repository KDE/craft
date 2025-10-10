import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/win-iconv/win-iconv.git"
        for ver in ["0.0.7", "0.0.8", "0.0.10"]:
            self.targets[ver] = f"https://github.com/win-iconv/win-iconv/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"win-iconv-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"win-iconv-{ver}"
        self.patchToApply["0.0.8"] = [("iconv-0.0.8-20250413.diff", 1)]
        self.patchToApply["0.0.10"] = [("iconv-0.0.8-20250413.diff", 1)]

        self.targetDigests["0.0.8"] = (["23adea990a8303c6e69e32a64a30171efcb1b73824a1c2da1bbf576b0ae7c520"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.0.10"] = (["58493387c7c9c70d61e711ec2feec5db0a59d164556642d2b427dde4ef756bc1"], CraftHash.HashAlgorithm.SHA256)

        self.description = "a character set conversion library binary compatible with GNU iconv"
        self.defaultTarget = "0.0.10"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False
