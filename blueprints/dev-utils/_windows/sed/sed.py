import info
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.1.5", "4.2.1"]:
            self.targets[ver] = [
                f"http://downloads.sourceforge.net/sourceforge/gnuwin32/sed-{ver}-bin.zip",
                f"http://downloads.sourceforge.net/sourceforge/gnuwin32/sed-{ver}-dep.zip",
            ]
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["4.1.5"] = [
            "abe52d0be25f1bb44b8a8e7a94e7afa9c15b3ae5",
            "736678616305fab80b4ec1a639d5ff0170183310",
        ]
        self.targetDigests["4.2.1"] = [
            "dfd3d1dae27a24784d7ab40eb074196509fa48fe",
            "f7edbd7152d8720c95d46dd128b87b8ba48a5d6f",
        ]
        self.defaultTarget = "4.2.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False
