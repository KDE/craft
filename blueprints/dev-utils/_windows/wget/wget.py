import info
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        # temporarily disable until we got binaries
        self.parent.package.categoryInfo.platforms = CraftCompiler.Platforms.NoPlatform

    def setTargets(self):
        self.webpage = "https://gitlab.com/gnuwget/wget2"
        self.releaseManagerId = 234933

        for ver in ["2.3.0"]:
            # TODO: as the artifact  is not versioned, updates will complain about the checksum
            self.targets[ver] = f"https://github.com/rockdaboot/wget2/releases/download/v{ver}/wget2.exe"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.defaultTarget = "2.3.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/7zip"] = None
        self.buildDependencies["core/cacert"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
