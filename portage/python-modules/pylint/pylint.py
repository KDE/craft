# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    # def setDependencies( self ):

    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'


class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
        self.python2 = False

    def install(self):
        pythonPath = craftSettings.get("Paths", "PYTHON")
        utils.createShim(os.path.join(self.imageDir(), "bin", "pylint.exe"),
                         os.path.join(pythonPath, "scripts", "pylint"),
                         useAbsolutePath=True)
        return PipBuildSystem.install(self)
