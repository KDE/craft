import info
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.0", "2.2.1"]:
            # TODO: as the artifact  is not versioned, updates will complain about the checksum
            self.targets[ver] = f"https://github.com/rockdaboot/wget2/releases/download/v{ver}/wget2.exe"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targetDigests["2.1.0"] = (["aad2b280c0f54741a1e5a4b7be99fc48cf39a7fc21827d5ec69860b9e02e9f28"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.2.1"] = (["c65f66842888b878d1fad48294d1372553985b86613f279cf4ed9612c4f80428"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.2.1"

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
