# -*- coding: utf-8 -*-

import os

import info
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        for ver in ["1_0_14", "1_0_15", "1_0_16", "1_1_2", "1_1_3"]:
            self.targets[ver] = f"https://download.qt.io/official_releases/jom/jom_{ver}.zip"
            self.targetDigestUrls[ver] = (
                ["https://download.qt.io/official_releases/jom/md5sums.txt"],
                CraftHash.HashAlgorithm.MD5,
            )
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
        self.defaultTarget = "1_1_3"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
