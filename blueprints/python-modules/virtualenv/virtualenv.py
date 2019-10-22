# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):

    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["python-modules/pip"] = None

class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)

    def postInstall(self):
        for ver, python in self._pythons:
            if not self.venvDir(ver).exists():
                if not utils.system([python, "-m", "venv" if ver == "3" else "virtualenv", self.venvDir(ver)]):
                    return False
        return True
