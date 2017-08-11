# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:nepomukshell'
        self.defaultTarget = 'master'
        self.description = (
            "NepomukShell is a maintenance and debugging "
            "tool intended for developers. It allows to browse, "
            "query, and edit Nepomuk resources.")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt"] = "default"
        self.runtimeDependencies['kde/kdelibs'] = 'default'
        self.runtimeDependencies["kdesupport/soprano"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
