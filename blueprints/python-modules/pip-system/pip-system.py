import io
import subprocess

import info
import utils

from Package.PipPackageBase import PipPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None

class Package(PipPackageBase):
    def __init__(self):
        PipPackageBase.__init__(self)
        self.pipPackageName = "pip"

    def make(self):
        for ver, python in self._pythons:
            # if its installed we get the help text if not we get an empty string
            with io.StringIO() as tmp:
                utils.system([python, "-m", "pip"], stdout=tmp, stderr=subprocess.DEVNULL)
                if not tmp.getvalue():
                    if not utils.system([python, "-m", "ensurepip", "--user"]):
                        return False
        return True

