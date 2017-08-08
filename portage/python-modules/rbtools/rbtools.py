# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-util/python2"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = ''
        self.description = "Review Board Tools."
        self.defaultTarget = 'master'


class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
        self.python3 = False
        self.allowExternal = True

    def install(self):
        pythonPath = craftSettings.get("Paths", "PYTHON27")
        return PipBuildSystem.install(self) and utils.createShim(
            os.path.join(self.imageDir(), "bin", "rbt.exe"),
            os.path.join(pythonPath, "scripts", "rbt.exe"))
