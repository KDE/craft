import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/vonreth/kshim.git"
        self.patchLevel["master"] = 10
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["dev-utils/mingw-w64"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
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
            return utils.system([sys.executable, os.path.join(self.sourceDir(), "bootstrap.py")], cwd=self.buildDir())

    def install(self):
        if not self._botstrap:
            return super().install()
        else:
            return  utils.copyFile(os.path.join(self.buildDir(), f"kshimgen{CraftCore.compiler.executableSuffix}"), os.path.join(self.installDir(), "bin", f"kshimgen{CraftCore.compiler.executableSuffix}"))
