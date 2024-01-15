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
        self.buildDependencies["python-modules/pip-system"] = None
        self.buildDependencies["python-modules/virtualenv"] = None
        self.buildDependencies["python-modules/pip"] = None
        # Python modules needed by custom signing
        self.runtimeDependencies["python-modules/paramiko"] = None
        self.runtimeDependencies["python-modules/pyyaml"] = None
        self.runtimeDependencies["python-modules/requests"] = None


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
        python3 = Path(CraftCore.standardDirs.etcDir()) / f"virtualenv/3/{binDir}/python{CraftCore.compiler.executableSuffix}"
        return utils.createShim(
            os.path.join(self.installDir(), "bin", f"python{CraftCore.compiler.executableSuffix}"),
            python3,
            useAbsolutePath=True,
        ) and utils.createShim(
            os.path.join(
                self.installDir(),
                "bin",
                f"python3{CraftCore.compiler.executableSuffix}",
            ),
            python3,
            useAbsolutePath=True,
        )
