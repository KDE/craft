# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["15.0.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "15.0.0"
        self.releaseManagerId = 41376
        self.description = "Rich is a library for rich text and beautiful formatting in the terminal"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.buildDependencies["python-modules/poetry-core"] = None
        self.runtimeDependencies["libs/python"] = None
        self.runtimeDependencies["python-modules/markdown-it-py"] = None
        self.runtimeDependencies["python-modules/pygments"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
