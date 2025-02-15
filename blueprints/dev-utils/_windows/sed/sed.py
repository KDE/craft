# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.description = "Craft integration package for sed."
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None
        self.buildDependencies["dev-utils/git"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False

    def postInstall(self):
        gitPath = CraftCore.cache.findApplication("git")
        if not gitPath:
            return False
        gitPath = gitPath.parent

        return utils.createShim(
            self.imageDir() / "dev-utils/bin/sed",
            gitPath.parent / "usr/bin/sed.exe",
            useAbsolutePath=True,
        )
