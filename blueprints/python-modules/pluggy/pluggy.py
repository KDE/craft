# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.7.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "1.7.0"
        self.releaseManagerId = 7500
        self.description = "Distribution-building parts of Flit. See flit package for more information"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["dev-utils/system-python3"] = None
        self.buildDependencies["python-modules/setuptools"] = None
        self.buildDependencies["python-modules/setuptools-scm"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
