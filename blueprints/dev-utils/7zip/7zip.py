import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotFreeBSD

    def setTargets(self):
        for ver in ["1900"]:
            self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/7z{ver}-extra.zip"
            self.targetInstSrc[ver] = f"7z{ver}-extra"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        for ver in ["2103"]:
            self.targetInstallPath[ver] = os.path.join("dev-utils", "7z")
            if CraftCore.compiler.isWindows:
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{ver}/7z{ver}-extra.zip"
                self.targetInstSrc[ver] = f"7z{ver}-extra"
            else:
                suffix = ""
                if CraftCore.compiler.isLinux:
                    suffix = f"-{CraftCore.compiler.architecture}"
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/{ver}/7z{ver}-{'mac' if CraftCore.compiler.isMacOS else 'linux'}{suffix}.tar.xz"
            self.targetDigestUrls[ver] =  self.targets[ver] + ".sha256"

        self.targetDigests["1900"] =  (['c946aa64d8a83176d44959bd84b27f42d254c4050ff7e408c22f682193481b95'], CraftHash.HashAlgorithm.SHA256)


        self.description = "7-Zip is a file archiver with a high compression ratio."
        self.webpage = "http://www.7-zip.org/"
        self.defaultTarget = "2103"

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.shelveAble = False

    def postInstall(self):
        if self.subinfo.buildTarget == "1900":
            return True
        return utils.createShim(self.imageDir() / f"dev-utils/bin/7za{CraftCore.compiler.executableSuffix}" , self.installDir() /  ("7za.exe" if CraftCore.compiler.isWindows else "7zz"))

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
