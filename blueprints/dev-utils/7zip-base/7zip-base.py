import info
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= ~CraftCore.compiler.Platforms.FreeBSD

    def setTargets(self):
        self.description = "7-Zip is a file archiver with a high compression ratio."
        self.webpage = "http://www.7-zip.org/"
        self.releaseManagerId = 372314

        for ver in ["26.05"]:
            verNoDot = ver.replace(".", "")
            self.targetInstallPath[ver] = "dev-utils/7z"
            if CraftCore.compiler.platform.isWindows:
                self.targets[ver] = (
                    f"https://github.com/TheOneRing/7zipzip/releases/download/{ver}/7zip-extra-{ver}-{CraftCore.compiler.architecture.key.name.lower()}.zip"
                )
                self.targetDigestUrls[ver] = (f"https://github.com/TheOneRing/7zipzip/releases/download/{ver}/SHA256.txt", CraftHash.HashAlgorithm.SHA256)
            elif CraftCore.compiler.platform.isLinux:
                arch = "x64"
                if CraftCore.compiler.architecture & CraftCore.compiler.Architecture.arm:
                    arch = "arm64"
                self.targets[ver] = f"https://www.7-zip.org/a/7z{verNoDot}-linux-{arch}.tar.xz"
            else:
                self.targets[ver] = f"https://7-zip.org/a/7z{verNoDot}-mac.tar.xz"

        self.defaultTarget = "26.05"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def binaryArchiveName(self, **kwargs):
        # never use 7z to compress this package
        kwargs["fileType"] = ".tar.xz"
        return super().binaryArchiveName(**kwargs)
