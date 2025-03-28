# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>
import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        useCraftPython = self.options.isActive("libs/python")
        if useCraftPython:
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.description = "Setup a venv to be used by Craft in case libs/python is not used"

        self.svnTargets["master"] = ""
        self.defaultTarget = "master"

    def setDependencies(self):
        # use the system wide pip
        self.runtimeDependencies["python-modules/pip-system"] = None


class Package(PipPackageBase):
    # Theoretically this is more a virtual package or helper,
    # but we use PipPackageBase to have access to self._pythons
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fetc(self):
        return True

    def unpack(self):
        return True

    def configure(self):
        return True

    def make(self):
        return True

    def install(self):
        for ver, python in self._pythons:
            venvPath = self.venvDir(ver)
            if not venvPath.exists():
                if not utils.system([python, "-m", "venv", venvPath]):
                    return False
            else:
                CraftCore.log.info(f"venv at {venvPath} does already exist, nothing to do")
        return True

    def qmerge(self):
        return True
