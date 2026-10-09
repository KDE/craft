import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        useCraftPython = self.options.isActive("libs/python")
        if useCraftPython:
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.Native

    def setTargets(self):
        self.targets["3"] = ""
        self.patchLevel["3"] = 3
        self.targetInstallPath["3"] = "dev-utils"
        self.defaultTarget = "3"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None
        self.buildDependencies["python-modules/pip-system"] = None
        self.buildDependencies["python-modules/virtualenv"] = None
        self.buildDependencies["python-modules/pip"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not super().install():
            return False
        binDir = "Scripts" if CraftCore.compiler.platform.isWindows else "bin"
        python3 = CraftCore.standardDirs.etcDir() / f"virtualenv/3/{binDir}/python{CraftCore.compiler.platform.executableSuffix}"
        return utils.createShim(
            self.installDir() / f"bin/python{CraftCore.compiler.platform.executableSuffix}",
            python3,
            useAbsolutePath=True,
        ) and utils.createShim(
            self.installDir() / f"bin/python3{CraftCore.compiler.platform.executableSuffix}",
            python3,
            useAbsolutePath=True,
        )
