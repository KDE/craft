import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/sdk/kshim.git"

        for ver in ["0.5.2"]:
            self.targets[ver] = f"https://invent.kde.org/sdk/kshim/-/archive/v{ver}/kshim-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kshim-v{ver}"

        self.targetDigests["0.5.2"] = (
            ["2b8c0aab9f3eedade289b0bda1c63116c6eb1063144e963d22a8690eb5837aac"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = "0.5.2"

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
