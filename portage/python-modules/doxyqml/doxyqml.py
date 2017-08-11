# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-util/python2"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = ''
        self.description = "Doxyqml is an input filter for Doxygen, a documentation system for C++ and a few other languages."
        self.defaultTarget = 'master'


class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
        self.python3 = False

    def install(self):
        utils.createShim(os.path.join(self.imageDir(), "bin", "doxyqml.exe"),
                         os.path.join(self.imageDir(), "dev-utils", "bin", "python2.exe"),
                         args=os.path.join(craftSettings.get("Paths", "PYTHON27"), "Scripts", "doxyqml"))
        return PipBuildSystem.install(self)
