import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2025-09-09", "2026-05-14"]:
            self.targets[ver] = f"https://files.kde.org/craft/curl.haxx.se/cacert-{ver}.zip"
            self.targetInstallPath[ver] = "etc"
        self.targetDigests["2025-09-09"] = (
            ["d1cdec8c94242b239123d2071fe5c1bf3d02b3c8c0c11ab7a994d9ae6281ff8e"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.webpage = "https://curl.haxx.se/docs/caextract.html"
        self.defaultTarget = "2026-05-14"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self):
        with utils.ScopedEnv({"SSL_CERT_FILE": None, "REQUESTS_CA_BUNDLE": None}):
            return super().fetch()
