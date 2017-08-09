# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(packageName="cfe", gitUrl="[git]https://git.llvm.org/git/clang.git")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/libxml2"] = "default"
        self.runtimeDependencies["win32libs/llvm-meta/llvm"] = "default"


from Package.SourceOnlyPackageBase import *


class Package(SourceOnlyPackageBase):
    def __init__(self, **args):
        SourceOnlyPackageBase.__init__(self)
