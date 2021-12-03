import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotFreeBSD & CraftCore.compiler.Platforms.NotAndroid
        self.options.dynamic.registerOption("useCentosBasedBuild", CraftCore.compiler.isLinux)

    def setTargets(self):
        for ver in ["2103"]:
            self.targetInstallPath[ver] = os.path.join("dev-utils", "7z")
            if not self.options.dynamic.useCentosBasedBuild:
                if CraftCore.compiler.isWindows:
                    self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{ver}/7z{ver}-extra.zip"
                    self.targetInstSrc[ver] = f"7z{ver}-extra"
                else:
                    suffix = ""
                    if CraftCore.compiler.isLinux:
                        suffix = f"-{CraftCore.compiler.architecture}"
                    self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{ver}/7z{ver}-{'mac' if CraftCore.compiler.isMacOS else 'linux'}{suffix}.tar.xz"
                self.targetDigestUrls[ver] =  self.targets[ver] + ".sha256"
            else:
                self.targets[ver] =  "https://github.com/fmoc/prebuilt-7z/releases/download/continuous/prebuilt-7z-21.03-x86_64.tar.gz"

        self.description = "7-Zip is a file archiver with a high compression ratio."
        self.webpage = "http://www.7-zip.org/"
        self.defaultTarget = "2103"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.shelveAble = False

    def unpack(self):
        if not super().unpack():
            return False
        if self.subinfo.options.dynamic.useCentosBasedBuild:
            return utils.deleteFile(self.localFilePath()[0])
        return True