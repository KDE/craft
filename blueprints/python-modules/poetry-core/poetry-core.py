# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.5.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "2.5.0"
        self.releaseManagerId = 71155
        self.webpage = "https://pypi.org/project/poetry-core/"
        self.description = "Poetry PEP 517 Build Backend"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
