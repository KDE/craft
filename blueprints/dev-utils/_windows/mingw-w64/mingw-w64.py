import info

class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NoPlatform

    def setTargets(self):
        for ver, rev, rt in [("8.1.0", "0", "6")]:
            arch = "i686" if CraftCore.compiler.isX86() else "x86_64"
            exceptionType = "sjlj" if CraftCore.compiler.isX86() else "seh"
            self.targets[f"{ver}-{rev}"] = f"https://files.kde.org/craft/3rdparty/mingw-builds/{arch}-{ver}-release-posix-{exceptionType}-rt_v{rt}-rev{rev}.zip"
            self.targetDigestUrls[f"{ver}-{rev}"] =  self.targets[f"{ver}-{rev}"] + ".sha256"

        for ver, rev, rt in [("11.2.0", "1", "9")]:
            #https://github.com/cristianadam/mingw-builds/releases/download/v11.2.0-rev1/x86_64-11.2.0-release-posix-seh-rt_v9-rev1.7z
            self.targets[f"{ver}-{rev}"] = f"https://github.com/cristianadam/mingw-builds/releases/download/v{ver}-rev{rev}/x86_64-{ver}-release-posix-seh-rt_v{rt}-rev{rev}.7z"
        self.targetDigests["11.2.0-1"] = (['ca41dd04e22cc1c4aca969726520383fad63fbdec5fa31c12095cb57f04c4757'], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.abi.startswith("mingw11"):
            self.defaultTarget = "11.2.0-1"
        else:
            self.defaultTarget = "8.1.0-0"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["dev-utils/7zip-base"] = None

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
