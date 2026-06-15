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
            ["f976dfe287484e786c899e2f009efc2ba290eb1cdb204a537ca89aa5a16700a7"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["2026-05-14"] = (
            ["b326c0143180f53da60034d229c741915aafda6bd5a5afdd253cc1f29a12993f"],
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
