import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/vonreth/kshim.git"
        for ver in ["0.1.0"]:
            self.targets[ver] = f"https://files.kde.org/craft/sources/libs/kshimgn/kshimgen-v{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kshimgen-v{ver}"
        self.targetDigests["0.1.0"] = (['1a46c599ca54e112fd37c39a60e5b97b6b20997e2114fe3cd422274c75ebcd22'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.1.0'

    def setDependencies(self):
        self.runtimeDependencies["dev-utils/mingw-w64"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if self.buildTarget == "master":
            self.subinfo.options.package.disableBinaryCache = True
            # can't be bootstrapped
            self.__botstrap = False
        else:
            self.__botstrap = None

    @property
    def _botstrap(self):
        if self.__botstrap is None:
            cmakeVer = CraftCore.cache.getVersion("cmake")
            self.__botstrap = not cmakeVer or cmakeVer < "3.8"
        return self.__botstrap

    def configure(self):
        if not self._botstrap:
            return super().configure()
        else:
            return True

    def make(self):
        if not self._botstrap:
            return super().make()
        else:
            utils.createDir(self.buildDir())
            return utils.system([sys.executable, os.path.join(self.sourceDir(), "bootstrap.py")], cwd=self.buildDir())

    def install(self):
        if not self._botstrap:
            return super().install()
        else:
            return  utils.copyFile(os.path.join(self.buildDir(), f"kshimgen{CraftCore.compiler.executableSuffix}"), os.path.join(self.installDir(), "bin", f"kshimgen{CraftCore.compiler.executableSuffix}"))
