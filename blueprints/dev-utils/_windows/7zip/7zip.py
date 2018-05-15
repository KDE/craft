import info
from Package.MaybeVirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1801", "1805"]:
            self.targets[ver] = f"https://files.kde.org/craft/3rdparty/7zip/7z{ver}-extra.zip"
            self.targetInstSrc[ver] = f"7z{ver}-extra"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

        self.targetInstallPath["1604.1"] = os.path.join("dev-utils", "bin")
        self.targets["1604.1"] = f"https://files.kde.org/craft/3rdparty/7zip/7z1604-extra.zip"

        self.targetDigests["1604.1"] = (["350a20ec1a005255713c39911982bdeb091fc94ad9800448505c4772f8e85074"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1801"] = (["094c1120f3af512855e1c1df86c5f170cb649f2ca97a23834ccebc04ba575a7a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1805"] = (["74c82814716d0b9e4769e4e4f1ac0c05ed08a2d6c77104ee398cafe3e73832ba"], CraftHash.HashAlgorithm.SHA256)

        self.description = "7-Zip is a file archiver with a high compression ratio."
        self.webpage = "http://www.7-zip.org/"
        self.defaultTarget = "1805"

from Package.BinaryPackageBase import *


class SevenZipPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if CraftCore.compiler.isX64():
            return utils.copyFile(os.path.join(self.sourceDir(), "x64", "7za.exe"),
                                  os.path.join(self.installDir(), "7za.exe"), linkOnly=False)
        else:
            return utils.copyFile(os.path.join(self.sourceDir(), "7za.exe"), os.path.join(self.installDir(), "7za.exe"),
                                  linkOnly=False)

    def postQmerge(self):
        CraftCore.cache.clear()


class Package(VirtualIfSufficientVersion):
    def __init__(self):
        VirtualIfSufficientVersion.__init__(self, app="7za", version="16.04", versionCommand="-version",
                                            classA=SevenZipPackage)
