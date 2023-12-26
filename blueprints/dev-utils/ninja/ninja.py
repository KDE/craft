# -*- coding: utf-8 -*-

import sys

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        """ """
        self.svnTargets["master"] = "https://github.com/martine/ninja.git"

        for ver in ["1.10.0", "1.10.2", "1.11.0", "1.11.1"]:
            self.targets[ver] = f"https://github.com/ninja-build/ninja/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"ninja-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ninja-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["1.10.0"] = (
            ["3810318b08489435f8efc19c05525e80a993af5a55baa0dfeae0465a9d45f99f"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.10.2"] = (
            ["ce35865411f0490368a8fc383f29071de6690cbadc27704734978221f25e2bed"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.11.1"] = (
            ["31747ae633213f1eda3842686f83c2aa1412e0f5691d1c14dbbcc67fe7400cea"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.patchToApply["1.10.0"] = [("34d1bf2f1dcc138f7cb3a54daf771931cd799785.patch", 1)]
        self.patchLevel["1.10.0"] = 1
        self.patchLevel["1.11.1"] = 1

        self.defaultTarget = "1.11.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/mingw-w64"] = None
        self.buildDependencies["dev-utils/cmake"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # building ninja with jom is broken
        self.subinfo.options.make.supportsMultijob = not CraftCore.compiler.isWindows
