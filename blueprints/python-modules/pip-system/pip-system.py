# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>
from Blueprints.CraftPackageObject import CraftPackageObject
from Package.PipPackageBase import PipPackageBase

pipPackage = CraftPackageObject.get("python-modules/pip")
subinfo = pipPackage.subinfo.__class__


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipPackageName = "pip"
        self.allowNotVenv = True
        self.unpack = pipPackage.instance.unpack
        self.make = pipPackage.instance.make
