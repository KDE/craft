import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1604.1"]:
            self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/7z1604-extra.zip"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        self.targetDigests["1604.1"] = (["350a20ec1a005255713c39911982bdeb091fc94ad9800448505c4772f8e85074"], CraftHash.HashAlgorithm.SHA256)

        self.description = "7-Zip is a file archiver with a high compression ratio."
        self.webpage = "http://www.7-zip.org/"
        self.defaultTarget = "1604.1"

from Package.BinaryPackageBase import *


class SevenZipPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        CraftCore.cache.clear()
        if craftCompiler.isX64():
            return utils.copyFile(os.path.join(self.sourceDir(), "x64", "7za.exe"),
                                  os.path.join(self.installDir(), "7za.exe"), linkOnly=False)
        else:
            return utils.copyFile(os.path.join(self.sourceDir(), "7za.exe"), os.path.join(self.installDir(), "7za.exe"),
                                  linkOnly=False)


class Package(VirtualIfSufficientVersion):
    def __init__(self):
        VirtualIfSufficientVersion.__init__(self, app="7za", version="16.04", versionCommand="-version",
                                            classA=SevenZipPackage)
