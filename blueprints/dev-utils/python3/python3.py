import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3"] = ""
        self.patchLevel["3"] = 3
        self.targetInstallPath["3"] = "dev-utils"
        self.defaultTarget = "3"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None
        self.runtimeDependencies["python-modules/pip"] = None
        self.runtimeDependencies["python-modules/virtualenv"] = None

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        binDir = "bin"
        if CraftCore.compiler.isWindows:
            binDir = "Scripts"
        return utils.createShim(os.path.join(self.installDir(), "bin", f"python3{CraftCore.compiler.executableSuffix}"),
                                Path(CraftCore.standardDirs.etcDir()) / f"virtualenv/3/{binDir}/python{CraftCore.compiler.executableSuffix}",
                                useAbsolutePath=True)
