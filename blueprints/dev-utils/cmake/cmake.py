import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.description = "Craft integration package for cmake."
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake-base"] = None
        self.buildDependencies["dev-utils/kshimgen"] = None


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not super().install():
            return False
        binaryPath = os.path.join(CraftCore.standardDirs.craftRoot(), "dev-utils", "cmake-base", "bin")
        if OsUtils.isMac():
            binaryPath = os.path.join(CraftCore.standardDirs.craftRoot(), "dev-utils", "cmake-base", "CMake.app", "Contents", "bin")

        for name in ["cmake", "cmake-gui", "cmcldeps", "cpack", "ctest"]:
            sourceBinary = os.path.join(binaryPath, f"{name}{CraftCore.compiler.executableSuffix}")
            targetBinary = os.path.join(self.imageDir(), "dev-utils", "bin", f"{name}{CraftCore.compiler.executableSuffix}")
            if os.path.exists(sourceBinary):
                if not utils.createShim(targetBinary, sourceBinary, useAbsolutePath=True):
                    return False
        return True

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
