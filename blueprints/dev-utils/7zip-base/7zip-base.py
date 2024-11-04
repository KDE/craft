import info
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= ~CraftCore.compiler.Platforms.FreeBSD

    def setTargets(self):
        for ver in ["24.09"]:
            verNoDot = ver.replace(".", "")
            self.targetInstallPath[ver] = "dev-utils/7z"
            if CraftCore.compiler.platform.isWindows:
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{verNoDot}/7z{verNoDot}-extra.zip"
                self.targetInstSrc[ver] = f"7z{verNoDot}-extra"
                self.targetDigestUrls[ver] = self.targets[ver] + ".sha256"
            elif CraftCore.compiler.platform.isLinux:
                arch = "x64"
                if CraftCore.compiler.architecture & CraftCore.compiler.Architecture.arm:
                    arch = "arm64"
                self.targets[ver] = f"https://www.7-zip.org/a/7z{verNoDot}-linux-{arch}.tar.xz"
            else:
                self.targets[ver] = f"https://7-zip.org/a/7z{verNoDot}-mac.tar.xz"
        self.description = "7-Zip is a file archiver with a high compression ratio."
        self.webpage = "http://www.7-zip.org/"
        self.defaultTarget = "24.09"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def binaryArchiveName(self, **kwargs):
        # never use 7z to compress this package
        if CraftCore.compiler.platform.isWindows:
            kwargs["fileType"] = ".zip"
        else:
            kwargs["fileType"] = ".tar.xz"

        return super().binaryArchiveName(**kwargs)
