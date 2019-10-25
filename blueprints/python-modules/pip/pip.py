import subprocess

import info
import utils

from Package.PipPackageBase import PipPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.4"]:
            self.targets[ver] = f"https://bootstrap.pypa.io/3.4/get-pip.py"
            self.targetDigests[ver] = (['b86f36cc4345ae87bfd4f10ef6b2dbfa7a872fbff70608a1e43944d283fd0eee'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.4"

class Package(PipPackageBase):
    def __init__(self):
        PipPackageBase.__init__(self)

    def unpack(self):
        return True

    def make(self):
        get_pip = self.localFilePath()[0]
        for ver, python in self._pythons:
            hasPip = utils.system([python, "-m", "pip"], stdout=subprocess.DEVNULL)
            if hasPip:
                continue
            if not utils.system([python, get_pip, "--user"]):
                return False
        return True

