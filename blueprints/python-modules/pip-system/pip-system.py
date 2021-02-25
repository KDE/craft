import io
import subprocess

import info
import utils

from Package.PipPackageBase import PipPackageBase
from Utils import CraftHash

import sys


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.4", "3.5"]:
            self.targets[ver] = f"https://bootstrap.pypa.io/3.5/get-pip.py"
            self.archiveNames[ver] = f"get-pip-{ver}.py"
        self.targetDigests["3.5"] = (['311afebb7cdd310eb3a3a6bb6fffef53d84493db98c7cebf4008a18d3418c8be'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.4"] = (['564fabc2fbabd9085a71f4a5e43dbf06d5ccea9ab833e260f30ee38e8ce63a69'], CraftHash.HashAlgorithm.SHA256)
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
        return True

