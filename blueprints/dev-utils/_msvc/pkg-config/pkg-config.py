import info
import utils
from CraftCompiler import CraftCompiler
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedBuild(
            "https://files.kde.org/craft/prebuilt/packages/22.11",
            packageName="dev-utils/_autotools/pkg-config",
            targetInstallPath="dev-utils",
            architecture=CraftCompiler.Architecture.x86_64,
        )

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        return utils.createShim(self.imageDir() / "dev-utils/bin/pkg-config.exe", self.installDir() / "bin/pkg-config.exe")
