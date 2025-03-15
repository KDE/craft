# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["1.27.0"] = ""
        self.defaultTarget = "1.27.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/setuptools"] = None
        self.buildDependencies["python-modules/packaging"] = None
        self.buildDependencies["python-modules/pathspec"] = None
        self.buildDependencies["python-modules/pluggy"] = None
        self.buildDependencies["python-modules/trove-classifiers"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--use-deprecated=legacy-resolver"]
