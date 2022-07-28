import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotFreeBSD & CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["21.03", "21.06", "21.07", "22.01"]:
            verNoDot = ver.replace(".", "")
            self.targetInstallPath[ver] = os.path.join("dev-utils", "7z")
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{verNoDot}/7z{verNoDot}-extra.zip"
                self.targetInstSrc[ver] = f"7z{verNoDot}-extra"
                self.targetDigestUrls[ver] =  self.targets[ver] + ".sha256"
            elif CraftCore.compiler.isLinux:
                self.targets[ver] =  f"https://github.com/fmoc/prebuilt-7z/releases/download/continuous/prebuilt-7z-{ver}-x86_64-asm.tar.gz"
            else:
                suffix = ""
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{verNoDot}/7z{verNoDot}-{'mac' if CraftCore.compiler.isMacOS else 'linux'}{suffix}.tar.xz"
                self.targetDigestUrls[ver] =  self.targets[ver] + ".sha256"


        self.description = "7-Zip is a file archiver with a high compression ratio."
        self.webpage = "http://www.7-zip.org/"
        self.defaultTarget = "22.01"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.shelveAble = False

    def unpack(self):
        if not super().unpack():
            return False
        if CraftCore.compiler.isLinux:
            return utils.deleteFile(self.localFilePath()[0])
        return True
