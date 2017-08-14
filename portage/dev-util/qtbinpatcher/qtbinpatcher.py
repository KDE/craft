# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/gonboy/QtBinPatcher.git"
        self.targetInstallPath["master"] = "dev-utils"
        for ver in ["2.2.0"]:
            self.targets[ver] = f"https://github.com/gonboy/QtBinPatcher/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qtbinpatcher-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qtbinpatcher-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["2.2.0"] = (
            ["7196199cd59777bf78ee0e3f77baa3c44e02e69dded192d6f0e59cf9b7bbd18e"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.2.0"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
