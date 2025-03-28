# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        useCraftPython = self.options.isActive("libs/python")
        if useCraftPython:
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        pip = CraftPackageObject.get("python-modules/pip").instance.subinfo

        for ver in pip.targets:
            self.targets[ver] = pip.targets[ver]
            self.targetDigests[ver] = pip.targetDigests[ver]
        self.defaultTarget = pip.defaultTarget

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True
        self.pipPackageName = "pip"
        self.allowNotVenv = True

    def unpack(self):
        return self.checkDigest(3)

    def make(self):
        self.enterBuildDir()
        return True
