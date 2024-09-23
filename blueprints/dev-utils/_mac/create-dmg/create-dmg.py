import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/andreyvit/create-dmg.git"
        self.targetInstallPath["master"] = "dev-utils/create-dmg"
        self.targets["1.2.1"] = "https://github.com/create-dmg/create-dmg/archive/refs/tags/v1.2.1.tar.gz"
        self.targetInstallPath["1.2.1"] = "dev-utils/create-dmg"
        self.targetInstSrc["1.2.1"] = "create-dmg-1.2.1"
        self.targetDigests["1.2.1"] = (["434746a84ed7e4a04b1d1977503e2a23ff79dac480cb86b24aae7b112e3b7524"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A shell script to build fancy DMGs"
        self.webpage = "https://github.com/andreyvit/create-dmg"
        self.defaultTarget = "1.2.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        return utils.createShim(self.imageDir() / "dev-utils/bin/create-dmg", self.imageDir() / "dev-utils/create-dmg/create-dmg")
