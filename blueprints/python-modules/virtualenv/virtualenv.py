# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):

    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'

    def setDependencies(self):
        # install a system whide pip
        self.runtimeDependencies["python-modules/pip-system"] = None

class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)

    def postInstall(self):
        for ver, python in self._pythons:
            if not self.venvDir(ver).exists():
                if ver == "2":
                    if not utils.system([python, "-m", "virtualenv", self.venvDir(ver)]):
                        return False
                else:
                    if not utils.system([python, "-m", "venv", "--without-pip", self.venvDir(ver)]):
                        return False
        return True
