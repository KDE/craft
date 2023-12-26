import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2022-04-26", "2023-01-10"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc"

        self.targetDigests["2022-04-26"] = (
            ["725effe112dc7f13ed25343b7d94a478cff926ade3118f597fa5467f790110cb"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2023-01-10"] = (
            ["d31764d1cf86e457199e820d5f0880933e6b0058afa7b5db19f8a526a6634a18"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.webpage = "https://curl.haxx.se/docs/caextract.html"
        self.defaultTarget = "2023-01-10"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        with utils.ScopedEnv({"SSL_CERT_FILE": None, "REQUESTS_CA_BUNDLE": None}):
            return super().fetch()
