from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.runtimeDependencies["dev-utils/msys-base"] = None


class Package(BinaryPackageBase):
    def __init__(self):
        super().__init__()

    def postInstall(self):
        return utils.createShim(
            self.imageDir() / "dev-utils/bin/msys.exe",
            self.imageDir() / "dev-utils/bin/python3.exe",
            args=[CraftStandardDirs.craftBin() / "shells.py"],
            useAbsolutePath=False,
        )
