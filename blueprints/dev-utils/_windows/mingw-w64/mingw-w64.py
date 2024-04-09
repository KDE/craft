import info


class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NoPlatform

    def setTargets(self):
        for ver, rev, rt in [("13.2.0", "1", "11")]:
            # https://github.com/niXman/mingw-builds-binaries/releases/download/13.2.0-rt_v11-rev1/x86_64-13.2.0-release-posix-seh-ucrt-rt_v11-rev1.7z
            self.targets[
                f"{ver}-{rev}"
            ] = f"https://github.com/niXman/mingw-builds-binaries/releases/download/{ver}-rt_v{rt}-rev{rev}/x86_64-{ver}-release-posix-seh-ucrt-rt_v{rt}-rev{rev}.7z"
        self.targetDigests["13.2.0-1"] = (
            ["475ee72c5ce1bd54a3e3c334bdd3be5e6575334184fd9718013aa362c9819d2f"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = "13.2.0-1"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["dev-utils/7zip-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
