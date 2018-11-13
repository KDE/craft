import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.16"] = "https://src.fedoraproject.org/lookaside/extras/chrpath/chrpath-0.16.tar.gz/2bf8d1d1ee345fc8a7915576f5649982/chrpath-0.16.tar.gz"
        self.targetInstSrc["0.16"] = "chrpath-0.16"
        self.targetInstallPath["0.16"] = "dev-utils"
        self.description = "change the rpath or runpath in binaries ."
        self.defaultTarget = "0.16"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
