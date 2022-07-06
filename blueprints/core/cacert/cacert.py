import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2021-09-30", "2021-10-26", "2022-04-26"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc"
        self.targetDigests["2021-09-30"] = (['ad2045d0aa58d1fd9d5b46bf66496065184437f5fe5597e962c2051464a84e3e'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2021-10-26"] = (['80bd2d1ccb1e652061e049beb0566bdf25e41c4d7503f4f9d92581401144912c'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2022-04-26"] = (['725effe112dc7f13ed25343b7d94a478cff926ade3118f597fa5467f790110cb'], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://curl.haxx.se/docs/caextract.html"
        self.defaultTarget = "2022-04-26"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        with utils.ScopedEnv({"SSL_CERT_FILE" : None, "REQUESTS_CA_BUNDLE": None}):
            return super().fetch()

