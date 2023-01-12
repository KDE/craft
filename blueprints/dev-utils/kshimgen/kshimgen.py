import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/sdk/kshim.git"

        for ver in ["0.5.4"]:
            self.targets[ver] = f"https://invent.kde.org/sdk/kshim/-/archive/v{ver}/kshim-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kshim-v{ver}"

        self.targetDigests["0.5.3"] = (
            ["f0df8b089c8464335c9599c73b83704798ff1adbe18707e7e91fc058345dbb4e"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = "0.5.4"

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake-base"] = None
        self.buildDependencies["dev-utils/mingw-w64"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def configure(self):
        cmakePath = Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/cmake-base"
        if OsUtils.isMac():
            cmakePath /= "CMake.app/Contents/bin"
        else:
            cmakePath /= "bin"
        path = f"{cmakePath}{os.pathsep}{os.environ['PATH']}"
        with utils.ScopedEnv({"PATH": path}):
            return super().configure()
