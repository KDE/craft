import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2018-01-17", "2018-04-07"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc"
        self.targetDigests["2018-01-17"] = (["d4dd92eaf208c18ac8fcbe04aa37be0b83a0f7f21cb788699a3acebace891b38"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2018-04-07"] = (["d4989b605f083ff39a2c8220da5c0b3c5e1816a06635361ca777d4a4b4285cab"], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://curl.haxx.se/docs/caextract.html"
        self.defaultTarget = "2018-04-07"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

