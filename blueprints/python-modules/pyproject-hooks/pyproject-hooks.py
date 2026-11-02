# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.3"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "1.3.3"
        self.releaseManagerId = 387211
        self.webpage = "https://pypi.org/project/pyproject_hooks/"
        self.description = "Wrappers to call pyproject.toml-based build backend hooks"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/flit-core"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
