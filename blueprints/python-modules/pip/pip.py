import info
from Package.MaybeVirtualPackageBase import *

from pathlib import Path
import sys

from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["master"] = f"https://bootstrap.pypa.io/get-pip.py"
        self.defaultTarget = "master"

from Package.PipPackageBase import *

class PPackage(PipPackageBase):
    def __init__(self):
        PipPackageBase.__init__(self)

    def make(self):
        get_pip = self.localFilePath()[0]
        for ver, python in self._pythons:
            if not utils.system([python, get_pip, "--user"]):
                return False
        return utils.deleteFile(get_pip)


class PipPackage(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        root = Path(CraftCore.standardDirs.craftRoot())
        py = Path(sys.executable)
        MaybeVirtualPackageBase.__init__(self, condition=CraftCore.compiler.isMacOS or root in py.parents, classA=PPackage, classB=PipPackage)

