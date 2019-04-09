import info
from Package.MaybeVirtualPackageBase import *

from pathlib import Path
import sys

from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["master"] = f"https://bootstrap.pypa.io/get-pip.py"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class PPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        get_pip = self.localFilePathe()[0]
        return (utils.system([sys.executable, get_pip])
                and utils.deleteFile(get_pip))

class PipPackage(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        root = Path(CraftCore.standardDirs.craftRoot())
        py = Path(sys.executable)
        MaybeVirtualPackageBase.__init__(self, condition=root in py.parents, classA=PPackage, classB=PipPackage)

