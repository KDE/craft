# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["25.1.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "25.1.0"
        self.releaseManagerId = 274452
        self.webpage = "https://pypi.org/project/hatch-fancy-pypi-readme/"
        self.description = "Fancy PyPI READMEs with Hatch"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.runtimeDependencies["python-modules/hatchling"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
