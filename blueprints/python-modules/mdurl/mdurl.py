# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.1.2"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "0.1.2"
        self.releaseManagerId = 223069
        self.description = "Markdown URL utilities"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.buildDependencies["python-modules/flit-core"] = None
        self.runtimeDependencies["libs/python"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
