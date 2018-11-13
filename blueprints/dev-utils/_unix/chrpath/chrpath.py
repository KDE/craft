import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.16"] = "https://todo/chrpath-0.16.tar.gz"
        self.targetInstSrc["0.16"] = "chrpath-0.16"
        self.targetInstallPath["0.16"] = "dev-utils"
        self.description = "change the rpath or runpath in binaries ."
        self.webpage = "https://alioth.debian.org/projects/chrpath/"
        self.defaultTarget = "0.16"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
