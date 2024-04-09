import info


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


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.shelveAble = False

    def postInstall(self):
        args = []
        appPath = CraftCore.standardDirs.craftRoot() / "dev-utils/7z" / ("7za.exe" if CraftCore.compiler.isWindows else "7zz")
        if CraftCore.compiler.isMacOS and not CraftCore.compiler.isNative():
            args = ["-arch", CraftCore.compiler.hostArchitecture.name.lower(), str(appPath)]
            appPath = "arch"
        return utils.createShim(self.imageDir() / f"dev-utils/bin/7za{CraftCore.compiler.executableSuffix}", appPath, useAbsolutePath=True, args=args)

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
