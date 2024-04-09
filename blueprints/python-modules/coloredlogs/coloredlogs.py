import info
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.buildDependencies["dev-utils/python3"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.python2 = False
