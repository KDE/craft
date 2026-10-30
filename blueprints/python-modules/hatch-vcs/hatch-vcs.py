# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["latest"] = ""
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.runtimeDependencies["python-modules/hatchling"] = None
        self.runtimeDependencies["python-modules/setuptools-scm"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--use-deprecated=legacy-resolver"]
