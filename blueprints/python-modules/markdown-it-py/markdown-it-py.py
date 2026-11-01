# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.2.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "4.2.0"
        self.releaseManagerId = 88959
        self.description = "Python port of markdown-it. Markdown parsing, done right!"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.buildDependencies["python-modules/flit-core"] = None
        self.runtimeDependencies["libs/python"] = None
        self.runtimeDependencies["python-modules/mdurl"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
