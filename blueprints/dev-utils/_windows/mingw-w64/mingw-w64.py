import info

class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NoPlatform

    def setTargets(self):
        for ver, rev, rt in [("11.2.0", "4", "9"), ("12.1.0", "0", "10")]:
            #https://github.com/cristianadam/mingw-builds/releases/download/v11.2.0-rev1/x86_64-11.2.0-release-posix-seh-rt_v9-rev1.7z
            self.targets[f"{ver}-{rev}"] = f"https://github.com/cristianadam/mingw-builds/releases/download/v{ver}-rev{rev}/x86_64-{ver}-release-posix-seh-rt_v{rt}-rev{rev}.7z"
        self.targetDigests["11.2.0-4"] = (['01afee61056d30480c7758b043f667814b724181a21b1465da3e98d1551bfa4f'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["12.1.0-0"] = (['6e929c993c62819e0fc1ced58fad00fd4597ebe74b2f55d5026f06ff65c793a2'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "12.1.0-0"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["dev-utils/7zip-base"] = None

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
