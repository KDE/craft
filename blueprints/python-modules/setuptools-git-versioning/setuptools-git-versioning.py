# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.2.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "3.2.0"
        self.releaseManagerId = 119596
        self.webpage = "https://pypi.org/project/setuptools-git-versioning/"
        self.description = "Use git repo data for building a version number according to PEP-440"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/wheel"] = None
        self.runtimeDependencies["python-modules/packaging"] = None
        self.runtimeDependencies["python-modules/setuptools"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
