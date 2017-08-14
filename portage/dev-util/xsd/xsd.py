import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for version in ['4.0.0']:
            self.targets[
                version] = f"http://codesynthesis.com/download/xsd/{version[:3]}/windows/i686/xsd-{version}-i686-windows.zip"
            self.targetInstSrc[version] = f"xsd-{version}-i686-windows"
            self.targetInstallPath[version] = f"dev-utils/xsd"
        self.targetDigests['4.0.0'] = (
            ['73c478ea76c9847bdd292f4db80900b93a9798334687999e54e5796971f11dc1'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '4.0.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "xsd.exe"),
                                os.path.join(self.imageDir(), "dev-utils", "xsd", "bin", "xsd.exe"))
