import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/vonreth/kshim.git"

        for ver in ["0.2.0"]:
            self.targets[ver] = f"https://files.kde.org/craft/sources/libs/kshimgn/kshimgen-v{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kshimgen-v{ver}"
        for ver in ["0.3.0", "0.4.0", "0.4.1", "0.4.2", "0.4.3"]:
            self.targets[ver] = f"https://invent.kde.org/vonreth/kshim/-/archive/v{ver}/kshim-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kshim-v{ver}"
        self.targetDigests["0.1.0"] = (['1a46c599ca54e112fd37c39a60e5b97b6b20997e2114fe3cd422274c75ebcd22'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.2.0"] =  (['b5f93d81d6937edb6608b87e0a87c9b7783aa7488c350683865beac3207d4312'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.3.0"] = (['1d5fee6e0cef513cbdef755b1829af2fe78be96eb88fa53a68594bfac0be7b0a'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.4.0"] = (['b59bea7b02ba2c37efbdba5706abe48f32fa3ca44b5a5f4e182ba8cdbadf0a32'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.4.1"] = (['a8d89683a89bffc1320273e1150a687745621231e1392bef04e89186b3f6cad9'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.4.2"] = (['ce3f203c6a682cc69e876f2c56e912aace30d9483f73d376441f356d4ea247f2'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.4.3"] = (['ebc514f9a07995c93d4ab7e2c10003ad42c41199572691cb92a506d546c2d340'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["0.2.0"] = 1
        self.defaultTarget = '0.4.3'

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake-base"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def configure(self):
        cmakePath = Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/cmake-base"
        if OsUtils.isMac():
            cmakePath /=  "CMake.app/Contents/bin"
        else:
            cmakePath /= "bin"
        path = f"{cmakePath}{os.pathsep}{os.environ['PATH']}"
        with utils.ScopedEnv({"PATH":path}):
            return super().configure()
