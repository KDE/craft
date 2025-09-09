import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.description = "Craft integration package for cmake."
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not super().install():
            return False
        cmakePath = CraftCore.standardDirs.craftRoot() / "dev-utils/cmake-base"
        if CraftCore.compiler.platform.isMacOS:
            cmakePath /= "CMake.app/Contents/bin"
        else:
            cmakePath /= "bin"

        for name in ["cmake", "cmake-gui", "cmcldeps", "cpack", "ctest"]:
            args = []
            sourceBinary = cmakePath / f"{name}{CraftCore.compiler.platform.executableSuffix}"
            targetBinary = self.imageDir() / f"dev-utils/bin/{name}{CraftCore.compiler.platform.executableSuffix}"
            if sourceBinary.exists():
                if not utils.createShim(targetBinary, sourceBinary, useAbsolutePath=True, args=args):
                    return False
        return True

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
