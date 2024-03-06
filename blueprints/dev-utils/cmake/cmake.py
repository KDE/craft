import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = (
            CraftCore.compiler.Platforms.Windows | CraftCore.compiler.Platforms.MacOS | CraftCore.compiler.Platforms.Linux
        )

    def setTargets(self):
        self.targets["latest"] = ""
        self.description = "Craft integration package for cmake."
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not super().install():
            return False
        cmakePath = Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/cmake-base"
        if OsUtils.isMac():
            cmakePath /= "CMake.app/Contents/bin"
        else:
            cmakePath /= "bin"

        for name in ["cmake", "cmake-gui", "cmcldeps", "cpack", "ctest"]:
            args = []
            sourceBinary = cmakePath / f"{name}{CraftCore.compiler.executableSuffix}"
            targetBinary = self.imageDir() / f"dev-utils/bin/{name}{CraftCore.compiler.executableSuffix}"
            if sourceBinary.exists():
                if CraftCore.compiler.isMacOS and not CraftCore.compiler.isNative():
                    args = ["-arch", CraftCore.compiler.hostArchitecture.name.lower(), str(sourceBinary)]
                    sourceBinary = "arch"
                if not utils.createShim(targetBinary, sourceBinary, useAbsolutePath=True, args=args):
                    return False
        return True

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
