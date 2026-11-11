# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import os
import shutil
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.description = "Craft integration package for ssh-askpass, runs the system askpass without the Craft Qt environment."
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None

    @staticmethod
    def locateAskpass() -> Path | None:
        craftRoot = CraftCore.standardDirs.craftRoot().resolve()
        candidates = [os.environ.get("SSH_ASKPASS", ""), "ksshaskpass", "ssh-askpass", "/usr/lib/ssh/ssh-askpass", "/usr/libexec/openssh/ssh-askpass", "/usr/lib/openssh/gnome-ssh-askpass"]
        systemPath = os.pathsep.join(p for p in os.environ.get("PATH", "").split(os.pathsep) if p and not Path(p).resolve().is_relative_to(craftRoot))
        for candidate in candidates:
            if not candidate:
                continue
            found = shutil.which(candidate, path=systemPath)
            if found and not Path(found).resolve().is_relative_to(craftRoot):
                return Path(found)
        return None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False

    def postInstall(self):
        askpass = self.subinfo.locateAskpass()
        if not askpass:
            CraftCore.log.warning("No system ssh-askpass found, skipping askpass shim")
            return True
        env = {key: "" for key in ["LD_LIBRARY_PATH", "QT_PLUGIN_PATH", "QML2_IMPORT_PATH", "QML_IMPORT_PATH", "QT_DATA_DIRS"]}
        return utils.createShim(
            self.imageDir() / "dev-utils/bin/ssh-askpass",
            askpass,
            env=env,
            useAbsolutePath=True,
        )
