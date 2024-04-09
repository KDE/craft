import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotFreeBSD & CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["21.03", "21.06", "21.07", "22.01", "23.01"]:
            verNoDot = ver.replace(".", "")
            self.targetInstallPath[ver] = "dev-utils/7z"
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{verNoDot}/7z{verNoDot}-extra.zip"
                self.targetInstSrc[ver] = f"7z{verNoDot}-extra"
                self.targetDigestUrls[ver] = self.targets[ver] + ".sha256"
            elif CraftCore.compiler.isLinux:
                if CraftCore.compiler.architecture == CraftCore.compiler.Architecture.x86_64:
                    self.targets[ver] = f"https://github.com/fmoc/prebuilt-7z/releases/download/continuous/prebuilt-7z-{ver}-x86_64-asm.tar.gz"
                elif CraftCore.compiler.architecture & CraftCore.compiler.Architecture.arm:
                    self.targets[ver] = f"https://www.7-zip.org/a/7z{verNoDot}-linux-arm64.tar.xz"
                    self.targetDigests["23.01"] = (["34e938fc4ba8ca6a835239733d9c1542ad8442cc037f43ca143a119bdf322b63"], CraftHash.HashAlgorithm.SHA256)
            else:
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{verNoDot}/7z{verNoDot}-mac.tar.xz"
                self.targetDigestUrls[ver] = self.targets[ver] + ".sha256"
        self.patchLevel["23.01"] = 1
        self.description = "7-Zip is a file archiver with a high compression ratio."
        self.webpage = "http://www.7-zip.org/"
        self.defaultTarget = "23.01"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False

    def binaryArchiveName(self, **kwargs):
        # never use 7z to compress this package
        if CraftCore.compiler.isWindows:
            kwargs["fileType"] = ".zip"
        else:
            kwargs["fileType"] = ".tar.xz"

        return super().binaryArchiveName(**kwargs)

    def unpack(self):
        if not super().unpack():
            return False
        if CraftCore.compiler.isLinux:
            return utils.deleteFile(self.localFilePath()[0])
        return True
