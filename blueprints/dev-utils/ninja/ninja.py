# -*- coding: utf-8 -*-

import sys

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        """ """
        self.svnTargets['master'] = "https://github.com/martine/ninja.git"

        for ver in ["1.10.0"]:
            self.targets[ver] = f"https://github.com/ninja-build/ninja/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"ninja-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ninja-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests['1.10.0'] = (['3810318b08489435f8efc19c05525e80a993af5a55baa0dfeae0465a9d45f99f'], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["1.10.0"] = [("34d1bf2f1dcc138f7cb3a54daf771931cd799785.patch", 1)]
        self.patchLevel["1.10.0"] = 1

        self.defaultTarget = "1.10.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/mingw-w64"] = None
        self.buildDependencies["dev-utils/cmake"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
