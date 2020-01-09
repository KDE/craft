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
        self.targetDigests["0.1.0"] = (['1a46c599ca54e112fd37c39a60e5b97b6b20997e2114fe3cd422274c75ebcd22'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.2.0"] =  (['b5f93d81d6937edb6608b87e0a87c9b7783aa7488c350683865beac3207d4312'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["0.2.0"] = 1
        self.defaultTarget = '0.2.0'

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake-base"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def configure(self):
        path = f"{Path(CraftCore.standardDirs.craftRoot()) / 'dev-utils/cmake-base/bin'}{os.pathsep}{os.environ['PATH']}"
        with utils.ScopedEnv({"Path":path}):
            return super().configure()
