# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2026.9.21.13"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "2026.9.21.13"
        self.releaseManagerId = 88298
        self.webpage = "https://pypi.org/project/trove-classifiers/"
        self.description = "Distribution-building parts of Flit. See flit package for more information"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["dev-utils/system-python3"] = None
        self.buildDependencies["python-modules/setuptools"] = None
        self.buildDependencies["python-modules/calver"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--use-deprecated=legacy-resolver"]
