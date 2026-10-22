import re

import info
import utils
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.webpage = "https://curl.se/windows/"
        self.description = "curl for Windows, used by craft as a fallback downloader."

        arch = "win64a" if CraftCore.compiler.hostArchitecture.isArm64 else "win64"
        pattern = re.compile(rf'dl-([\d._]+)/curl-\1-{arch}-mingw\.zip"')
        versions = CraftCore.cache.getNightlyVersionsFromUrl(self.webpage, pattern)
        # fall back to a known good version if the page can't be reached, e.g. when offline
        ver = sorted(versions, key=CraftVersion)[-1] if versions else "8.23.0_4"

        self.targets[ver] = f"https://curl.se/windows/dl-{ver}/curl-{ver}-{arch}-mingw.zip"
        self.targetInstSrc[ver] = f"curl-{ver}-{arch}-mingw"
        self.targetInstallPath[ver] = "dev-utils/curl"
        self.targetDigestUrls[ver] = (
            f"https://curl.se/windows/dl-{ver}/curl-{ver}-{arch}-mingw.zip.txt",
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["dev-utils/7zip"] = None
        self.buildDependencies["dev-utils/kshimgen"] = None
        self.buildDependencies["core/cacert"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # the artifact is versioned, but a rebuild of the same version might change its checksum
        self.subinfo.shelveAble = False

    def postInstall(self):
        return utils.createShim(
            self.imageDir() / "dev-utils/bin/curl.exe",
            self.imageDir() / "dev-utils/curl/bin/curl.exe",
        )

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
