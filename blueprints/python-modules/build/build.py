# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>
import info
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["dev-utils/system-python3"] = None
        self.buildDependencies["python-modules/flit-core"] = None
        self.runtimeDependencies["python-modules/packaging"] = None
        self.runtimeDependencies["python-modules/pyproject-hooks"] = None
        if CraftCore.compiler.platform.isWindows:
            self.runtimeDependencies["python-modules/colorama"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
