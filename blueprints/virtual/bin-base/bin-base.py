import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'
        self.description = "deprecated: use virtual/base instead"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
