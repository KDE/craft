# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.9.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "1.9.0"
        self.releaseManagerId = 388662
        self.description = "Python interpreter discovery"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/hatchling"] = None
        self.buildDependencies["python-modules/hatch-vcs"] = None
        self.buildDependencies["python-modules/hatch-fancy-pypi-readme"] = None
        self.runtimeDependencies["python-modules/filelock"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
