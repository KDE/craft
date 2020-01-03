from CraftCore import CraftCore
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.buildDependencies["dev-utils/python3"] = None


class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
        self.python2 = False


