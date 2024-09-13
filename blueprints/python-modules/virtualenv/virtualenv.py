# -*- coding: utf-8 -*-
import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        useCraftPython = CraftPackageObject.get("libs/python").categoryInfo.isActive
        if useCraftPython:
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        # install a system whide pip
        self.runtimeDependencies["python-modules/pip-system"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allowNotVenv = True

    def install(self):
        if CraftCore.compiler.platform.isLinux:
            return True
        return super().install()

    def postInstall(self):
        for ver, python in self._pythons:
            if not self.venvDir(ver).exists():
                if not utils.system([python, "-m", "venv", self.venvDir(ver)]):
                    return False
        return True
