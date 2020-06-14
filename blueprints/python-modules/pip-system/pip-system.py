import subprocess

import info
import utils

from Package.PipPackageBase import PipPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.4"]:
            self.targets[ver] = f"https://bootstrap.pypa.io/3.4/get-pip.py"
            self.targetDigests[ver] = (['564fabc2fbabd9085a71f4a5e43dbf06d5ccea9ab833e260f30ee38e8ce63a69'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.4"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None

class Package(PipPackageBase):
    def __init__(self):
        PipPackageBase.__init__(self)
        self.pipPackageName = "pip"

    def unpack(self):
        return self.checkDigest()

    def make(self):
        get_pip = self.localFilePath()[0]
        for ver, python in self._pythons:
            hasPip = utils.system([python, "-m", "pip"], stdout=subprocess.DEVNULL)
            if hasPip:
                continue
            if not utils.system([python, get_pip, "--user"]):
                return False
        return True

