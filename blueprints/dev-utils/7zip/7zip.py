import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotFreeBSD & CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.targets["latest"] = ""
        self.description = "Craft integration package for 7z."
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None
        self.buildDependencies["dev-utils/7zip-base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.shelveAble = False

    def postInstall(self):
        args = []
        appPath = CraftCore.standardDirs.craftRoot() / "dev-utils/7z"
        if CraftCore.compiler.isWindows:
            # TODO: arm
            appPath /= "x64/7za.exe"
        else:
            appPath /= "7zz"
        if CraftCore.compiler.isMacOS and not CraftCore.compiler.isNative():
            args = ["-arch", CraftCore.compiler.hostArchitecture.name.lower(), str(appPath)]
            appPath = "arch"

        # on Windows, we expect the file to be called 7za, the same applies to craft itself.
        # on Unix most apps expect 7zz, create both for compatibility
        for alias in ["7za", "7zz"]:
            if not utils.createShim(self.imageDir() / f"dev-utils/bin/{alias}{CraftCore.compiler.executableSuffix}", appPath, useAbsolutePath=True, args=args):
                return False
        return True

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
