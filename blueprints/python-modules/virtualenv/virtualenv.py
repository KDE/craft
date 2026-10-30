# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    # NOTE: this package is a normal python package,
    # don't confuse it with "virtual/craft-venv" which creates a venv

    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/hatchling"] = None
        self.buildDependencies["python-modules/hatch-vcs"] = None
        self.buildDependencies["python-modules/hatch-fancy-pypi-readme"] = None
        self.runtimeDependencies["python-modules/distlib"] = None
        self.runtimeDependencies["python-modules/filelock"] = None
        self.runtimeDependencies["python-modules/platformdirs"] = None
        self.runtimeDependencies["python-modules/python-discovery"] = None
        self.runtimeDependencies["python-modules/packaging"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
