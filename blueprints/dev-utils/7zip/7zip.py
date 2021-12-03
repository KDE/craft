import info
class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Windows | CraftCore.compiler.Platforms.MacOS | CraftCore.compiler.Platforms.Linux 

    def setTargets(self):
        self.targets["latest"] = ""
        self.description = "Craft integration package for 7z."
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None
        self.buildDependencies["dev-utils/7zip-base"] = None


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def postInstall(self):
        appPath = CraftCore.standardDirs.craftRoot() / "dev-utils/7z"
        return utils.createShim(self.imageDir() / f"dev-utils/bin/7za{CraftCore.compiler.executableSuffix}" , appPath /  ("7za.exe" if CraftCore.compiler.isWindows else "7zz"), useAbsolutePath=True)

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
