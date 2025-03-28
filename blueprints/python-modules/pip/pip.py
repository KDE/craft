# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["25.0.1"] = "https://bootstrap.pypa.io/pip/zipapp/pip-25.0.1.pyz"
        self.targetDigests["25.0.1"] = (["0a7353fc4c345a9589c1cff7b59eb1868079d3de5c2663846bcb4290a69e3b41"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["25.0.1"] = 1
        self.defaultTarget = "25.0.1"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["virtual/craft-venv"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def unpack(self):
        return self.checkDigest(3)

    def make(self):
        self.enterBuildDir()
        return True

    def install(self):
        return super().install() and self.createMacOSPipShims(["pip", "pip3"])
