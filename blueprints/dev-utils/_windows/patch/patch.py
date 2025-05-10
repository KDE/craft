# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>

import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.description = "Craft integration package for patch."
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None
        self.buildDependencies["dev-utils/uactools"] = None
        self.buildDependencies["dev-utils/git"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False
        self.subinfo.options.package.disableBinaryCache = True

    def postInstall(self):
        gitPath = CraftPackageObject.get("dev-utils/git").subinfo.locateGit()

        # TODO: kshimgen should copy the manifest
        return utils.createShim(
            self.imageDir() / "dev-utils/bin/patch.exe",
            gitPath.parent / "usr/bin/patch.exe",
            useAbsolutePath=True,
        ) and utils.embedManifest(self.imageDir() / "dev-utils/bin/patch.exe", self.blueprintDir() / "patch.manifest")
