import io
import subprocess

import info
import utils

from Package.PipPackageBase import PipPackageBase
from Utils import CraftHash

import sys


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.5"]:
            self.targets[ver] = f"https://bootstrap.pypa.io/3.5/get-pip.py"
            self.targetDigests[ver] = (['dbd5dae3d1e7f6df844d630cdf65e0f0d98e483c9997daea17c7c9d86f7b38ad'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.5"

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
        # if its installed we get the help text if not we get an empty string
        with io.StringIO() as tmp:
            utils.system([sys.executable, "-m", "pip"], stdout=tmp, stderr=subprocess.DEVNULL)
            if tmp.getvalue():
                return True
        if not utils.system([sys.executable, get_pip, "--user"]):
            return False

