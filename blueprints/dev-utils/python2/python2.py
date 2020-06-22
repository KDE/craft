import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["2"] = ""
        self.defaultTarget = "2"
        self.targetInstallPath["2"] = "dev-utils"
        self.patchLevel["2"] = 3

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True
    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        python2 = CraftCore.cache.findApplication("python2.7")
        if CraftCore.compiler.isWindows:
                exitCode, _python2 = CraftCore.cache.getCommandOutput("py", "-2 -c \"import sys; print(sys.executable)\"")
                if exitCode == 0:
                    python2 = _python2.strip()
                if not python2 and ("Paths", "PYTHON27") in CraftCore.settings:
                    python2 = CraftCore.cache.findApplication("python", CraftCore.settings.get("Paths", "PYTHON27"))
        if not python2:
            CraftCore.log.critical(f"Please have a look on {CraftCore.settings.iniPath} and make sure that\n"
                                   "\t[Paths]\n"
                                   "\tPYTHON27\n"
                                   "Points to a valid Python installation.")
            return False
        return (utils.createShim(os.path.join(self.installDir(), "bin", f"python{CraftCore.compiler.executableSuffix}"), python2, useAbsolutePath=True) and
                utils.createShim(os.path.join(self.installDir(), "bin", f"python2{CraftCore.compiler.executableSuffix}"), python2, useAbsolutePath=True))

