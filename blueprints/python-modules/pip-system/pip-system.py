import io
import subprocess

import info
import utils
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipPackageName = "pip"
        self.allowNotVenv = True

    def make(self):
        for ver, python in self._pythons:
            # if its installed we get the help text if not we get an empty string
            with io.StringIO() as tmp:
                utils.system([python, "-m", "pip"], stdout=tmp, stderr=subprocess.DEVNULL)
                if not tmp.getvalue():
                    if not utils.system([python, "-m", "ensurepip", "--user"]):
                        return False
        return True

    def install(self):
        if CraftCore.compiler.isLinux:
            return True
        return super().install()
