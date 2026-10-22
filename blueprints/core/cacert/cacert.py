import re

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.webpage = "https://curl.se/docs/caextract.html"

        pattern = re.compile(r'/ca/cacert-(\d{4}-\d{2}-\d{2})\.pem"')
        versions = CraftCore.cache.getNightlyVersionsFromUrl(self.webpage, pattern)
        # fall back to a known good version if the page can't be reached, e.g. when offline
        ver = max(versions) if versions else "2026-05-14"

        self.targets[ver] = f"https://curl.se/ca/cacert-{ver}.pem"
        self.targetInstallPath[ver] = "etc"
        self.targetDigestUrls[ver] = (
            f"https://curl.se/ca/cacert-{ver}.pem.sha256",
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = ver


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fetch(self):
        with utils.ScopedEnv({"SSL_CERT_FILE": None, "REQUESTS_CA_BUNDLE": None}):
            return super().fetch()

    def unpack(self):
        return self.checkDigest()

    def install(self):
        return utils.copyFile(self.localFilePath()[0], self.installDir() / "cacert.pem")
