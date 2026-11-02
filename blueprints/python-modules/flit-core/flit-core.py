# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.2.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "4.2.0"
        self.releaseManagerId = 44841
        self.webpage = "https://pypi.org/project/flit-core/"
        self.description = "Distribution-building parts of Flit. See flit package for more information"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
