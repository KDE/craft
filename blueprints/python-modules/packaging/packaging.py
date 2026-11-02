# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["26.3"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "26.3"
        self.releaseManagerId = 60461
        self.webpage = "https://pypi.org/project/packaging/"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["dev-utils/system-python3"] = None
        self.buildDependencies["python-modules/flit-core"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
