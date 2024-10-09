import info
import utils
from CraftStandardDirs import CraftStandardDirs
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.runtimeDependencies["dev-utils/msys-base"] = None
        self.runtimeDependencies["dev-utils/system-python3"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.shelveAble = False

    def postInstall(self):
        return utils.createShim(
            self.imageDir() / "dev-utils/bin/msys.exe",
            self.imageDir() / "dev-utils/bin/python3.exe",
            args=[CraftStandardDirs.craftBin() / "shells.py"],
            useAbsolutePath=False,
        )
