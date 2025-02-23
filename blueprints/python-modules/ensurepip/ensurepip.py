# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
import io
import subprocess

import info
import utils
from Package.PackageBase import PackageBase
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["core/cacert"] = None
        self.buildDependencies["python-modules/virtualenv"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        for ver, python in self._pythons:
            # if its installed we get the help text if not we get an empty string
            with io.StringIO() as tmp:
                utils.system([python, "-m", "pip"], stdout=tmp, stderr=subprocess.DEVNULL)
                if tmp.getvalue():
                    return True

                if not utils.system([python, "-m", "ensurepip", "--upgrade", "--root", self.installDir()]):
                    return False
                if not self._fixInstallPrefix():
                    return False
        return True

    # don't actually install the files
    def qmerge(self):
        return PackageBase.qmerge(self, dbOnly=True)
