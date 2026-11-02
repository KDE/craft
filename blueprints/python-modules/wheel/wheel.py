# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.48.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "0.48.0"
        self.releaseManagerId = 11428
        self.webpage = "https://github.com/pypa/wheel"
        self.description = "Command line tool for manipulating wheel files"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/flit-core"] = None
        self.runtimeDependencies["python-modules/packaging"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
