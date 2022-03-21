import info

class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NoPlatform

    def setTargets(self):
        for ver, rev, rt in [("11.2.0", "3", "9")]:
            #https://github.com/cristianadam/mingw-builds/releases/download/v11.2.0-rev1/x86_64-11.2.0-release-posix-seh-rt_v9-rev1.7z
            self.targets[f"{ver}-{rev}"] = f"https://github.com/cristianadam/mingw-builds/releases/download/v{ver}-rev{rev}/x86_64-{ver}-release-posix-seh-rt_v{rt}-rev{rev}.7z"
        self.targetDigests["11.2.0-3"] = (['152c6d28deb7107ac67257bb21edf80f650b85567c5baf9a23d211a35dfbcc49'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "11.2.0-3"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["dev-utils/7zip-base"] = None

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
