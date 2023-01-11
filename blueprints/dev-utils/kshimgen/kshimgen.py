import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/sdk/kshim.git"

        for ver in ["0.5.3"]:
            self.targets[ver] = f"https://invent.kde.org/sdk/kshim/-/archive/v{ver}/kshim-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kshim-v{ver}"

        self.targetDigests["0.5.3"] = (
            ["7037c0d009240f1a20d6197e4d3a50195740837c3d851347b3da974742d64a39"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = "0.5.3"

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
