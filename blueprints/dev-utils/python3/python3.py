import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3"] = ""
        self.patchLevel["3"] = 1
        self.targetInstallPath["3"] = "dev-utils"
        self.defaultTarget = "3"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        CraftCore.cache.clear()
        return (utils.createShim(os.path.join(self.installDir(), "bin", "python3.exe"),
                                sys.executable,
                                useAbsolutePath=True) and
                utils.createShim(os.path.join(self.installDir(), "bin", "python.exe"),
                                sys.executable,
                                useAbsolutePath=True))
