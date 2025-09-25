import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2023-01-10", "2023-12-12", "2025-09-09"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc"
        self.targetDigests["2023-01-10"] = (
            ["d31764d1cf86e457199e820d5f0880933e6b0058afa7b5db19f8a526a6634a18"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2023-12-12"] = (
            ["e7d3215c9e1273056e7beea4f84d2c7b22b22ff0b15c5c88ce2e3f857e6a45ea"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2025-09-09"] = (
            ["f976dfe287484e786c899e2f009efc2ba290eb1cdb204a537ca89aa5a16700a7"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.webpage = "https://curl.haxx.se/docs/caextract.html"
        self.defaultTarget = "2025-09-09"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        with utils.ScopedEnv({"SSL_CERT_FILE": None, "REQUESTS_CA_BUNDLE": None}):
            return super().fetch()
