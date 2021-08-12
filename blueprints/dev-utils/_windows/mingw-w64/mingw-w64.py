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
        self.defaultTarget = "8.1.0-0"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
