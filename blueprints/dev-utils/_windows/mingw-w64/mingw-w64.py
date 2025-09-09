import info
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler &= CraftCore.compiler.Compiler.MinGW

    def setTargets(self):
        for ver, rev, rt in [("13.2.0", "1", "11"), ("14.2.0", "1", "12"), ("14.2.0", "2", "12")]:
            # https://github.com/niXman/mingw-builds-binaries/releases/download/13.2.0-rt_v11-rev1/x86_64-13.2.0-release-posix-seh-ucrt-rt_v11-rev1.7z
            self.targets[
                f"{ver}-{rev}"
            ] = f"https://github.com/niXman/mingw-builds-binaries/releases/download/{ver}-rt_v{rt}-rev{rev}/x86_64-{ver}-release-posix-seh-ucrt-rt_v{rt}-rev{rev}.7z"
        self.targetDigests["13.2.0-1"] = (
            ["475ee72c5ce1bd54a3e3c334bdd3be5e6575334184fd9718013aa362c9819d2f"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["14.2.0-1"] = (
            ["9fa5768ba0e628203c4631d447ce533335cdd1fd9c318d84c774e729efa4edad"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["14.2.0-2"] = (
            ["918732a84fc8006586be0f5909b75896ab85d5e0e9df521b4d4f9202e7debc12"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = "14.2.0-2"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["dev-utils/7zip-base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
