# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>

import info
from CraftCore import CraftCore
from Package.MsysPackageBase import MsysPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Windows
        self.parent.package.categoryInfo.architecture = CraftCore.compiler.CompilerFilter()

    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.runtimeDependencies["dev-utils/msys-base"] = None
        self.buildDependencies["dev-utils/m4"] = None


class Package(MsysPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.msysPackages = ["msys/autoconf-wrapper"]
