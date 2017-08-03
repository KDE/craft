# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/llvm-meta/clang"] = "default"


from Package.SourceOnlyPackageBase import *


class Package(SourceOnlyPackageBase):
    def __init__(self, **args):
        SourceOnlyPackageBase.__init__(self)
