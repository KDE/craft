import info
import utils
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.webpage = "https://curl.se/docs/caextract.html"

        for ver in ["2026-10-20"]:
            self.targets[ver] = f"https://curl.se/ca/cacert-{ver}.pem"
            self.targetInstallPath[ver] = "etc"
            self.targetDigestUrls[ver] = (
                f"https://curl.se/ca/cacert-{ver}.pem.sha256",
                CraftHash.HashAlgorithm.SHA256,
            )
        self.defaultTarget = "2026-10-20"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryArchive = True

    def fetch(self):
        with utils.ScopedEnv({"SSL_CERT_FILE": None, "REQUESTS_CA_BUNDLE": None}):
            return super().fetch()

    def unpack(self):
        return self.checkDigest()

    def install(self):
        return utils.copyFile(self.localFilePath()[0], self.installDir() / "cacert.pem")

    def binaryArchiveName(self, **kwargs):
        # never use 7z to compress bootstrap package
        kwargs["fileType"] = ".tar.xz"
        return super().binaryArchiveName(**kwargs)
