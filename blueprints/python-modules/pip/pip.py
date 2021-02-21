import io
import subprocess

import info
import utils

from Package.PipPackageBase import PipPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.5"]:
            self.targets[ver] = f"https://bootstrap.pypa.io/3.5/get-pip.py"
            self.targetDigests[ver] = (['dbd5dae3d1e7f6df844d630cdf65e0f0d98e483c9997daea17c7c9d86f7b38ad'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.5"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.buildDependencies["python-modules/virtualenv"] = None

class Package(PipPackageBase):
    def __init__(self):
        PipPackageBase.__init__(self)

    def unpack(self):
        return self.checkDigest()

    def make(self):
        get_pip = self.localFilePath()[0]
        for ver, python in self._pythons:
            # if its installed we get the help text if not we get an empty string
            with io.StringIO() as tmp:
                utils.system([python, "-m", "pip"], stdout=tmp, stderr=subprocess.DEVNULL)
                if not tmp.getvalue():
                    if not utils.system([python, get_pip]):
                        return False
        return True

