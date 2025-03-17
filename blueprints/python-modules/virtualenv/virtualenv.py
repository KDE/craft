# -*- coding: utf-8 -*-
import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        # install a system whide pip
        self.runtimeDependencies["python-modules/pip-system"] = None
        self.runtimeDependencies["python-modules/hatch-vcs"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allowNotVenv = True

    def postInstall(self):
        if not CraftPackageObject.get("libs/python").categoryInfo.isActive:
            for ver, python in self._pythons:
                if not self.venvDir(ver).exists():
                    if not utils.system([python, "-m", "venv", self.venvDir(ver)]):
                        return False
        return True
