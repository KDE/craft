import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2018-01-17"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc"
        self.targetDigests["2018-01-17"] = (["d4dd92eaf208c18ac8fcbe04aa37be0b83a0f7f21cb788699a3acebace891b38"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2018-01-17"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

