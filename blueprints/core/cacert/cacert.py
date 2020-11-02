import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2018-12-05", "2020-01-01", "2020-10-14"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc"
        self.targetDigests["2018-12-05"] = (['6e3a346aac36e271fc23d4476608226059e76ffd0a7645e2a1ba25937cf3df2e'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2020-01-01"] = (['db0d0ddc3ed80b0f4fd59077c266113c4e7e5c031bd1011c42d8495864418edd'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2020-10-14"] = (['c333bd1e49b76f56424a086e02524f7243a864c78e0fe95626da280cd94010cc'], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://curl.haxx.se/docs/caextract.html"
        self.defaultTarget = "2020-10-14"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        with utils.ScopedEnv({"SSL_CERT_FILE" : None, "REQUESTS_CA_BUNDLE": None}):
            return super().fetch()

