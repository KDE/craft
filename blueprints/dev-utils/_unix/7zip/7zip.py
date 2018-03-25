import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["16.02"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/sourceforge/p7zip/p7zip_{ver}_src_all.tar.bz2"
            self.targetInstSrc[ver] = f"p7zip_{ver}"
            self.targetInstallPath[ver] = "dev-utils"

        self.targetDigests["16.02"] = (['5eb20ac0e2944f6cb9c2d51dd6c4518941c185347d4089ea89087ffdd6e2341f'], CraftHash.HashAlgorithm.SHA256)

        self.description = "p7zip is a quick port of 7z.exe and 7za.exe for Unix."
        self.webpage = "https://sourceforge.net/projects/p7zip/"
        self.defaultTarget = "16.02"

from Package.MakeFilePackageBase import *


class Package(MakeFilePackageBase):
    def __init__(self):
        MakeFilePackageBase.__init__(self)
        self.subinfo.options.useShadowBuild = False

    def install(self):
        return utils.copyFile(os.path.join(self.sourceDir(), "bin", "7za"), os.path.join(self.installDir(), "bin", "7za"), linkOnly=False)
