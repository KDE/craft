import info
from CraftCompiler import CraftCompiler
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedBuild(
            "https://files.kde.org/craft/prebuilt/packages/22.11",
            packageName="dev-utils/_autotools/pkg-config",
            targetInstallPath="dev-utils",
            architecture=CraftCompiler.Architecture.x86_64,
        )

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = None


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def postInstall(self):
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "pkg-config.exe"), os.path.join(self.installDir(), "bin", "pkg-config.exe"))
