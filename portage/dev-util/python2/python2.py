import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["2"] = ""
        self.defaultTarget = "2"
        self.targetInstallPath["2"] = "dev-utils"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if not ("Paths", "PYTHON27") in craftSettings or \
                not os.path.isfile(os.path.join(craftSettings.get("Paths", "PYTHON27"), "python.exe")):
            craftDebug.log.critical(f"Please have a look on {craftSettings.iniPath} and make sure that\n"
                                    "\t[Paths]\n"
                                    "\tPYTHON27\n"
                                    "Points to a valid Python installation.")
            return False
        utils.utilsCache.clear()
        return utils.createShim(os.path.join(self.installDir(), "bin", "python2.exe"),
                                os.path.join(craftSettings.get("Paths", "PYTHON27"), "python.exe"),
                                useAbsolutePath=True)
