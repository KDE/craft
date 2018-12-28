import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2018-12-05"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc"
        self.targetDigests["2018-12-05"] = (['6e3a346aac36e271fc23d4476608226059e76ffd0a7645e2a1ba25937cf3df2e'], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://curl.haxx.se/docs/caextract.html"
        self.defaultTarget = "2018-12-05"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

