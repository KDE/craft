import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["2"] = ""
        self.defaultTarget = "2"
        self.targetInstallPath["2"] = "dev-utils"
        self.patchLevel["2"] = 2

    def setDependencies(self):
        self.runtimeDependencies["python-modules/pip"] = None
        self.runtimeDependencies["python-modules/virtualenv"] = None

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        return utils.createShim(os.path.join(self.installDir(), "bin", f"python2{CraftCore.compiler.executableSuffix}"),
                                Path(CraftCore.standardDirs.etcDir()) / f"venv/2/Scripts/python{CraftCore.compiler.executableSuffix}",
                                useAbsolutePath=True)