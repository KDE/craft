# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import re
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.description = (
            "Compatibility package to provide a libcrypt.so.2 symlink on systems that ship the .so.1 that contains the new api and the legacy apis."
        )
        self.defaultTarget = "latest"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True

    def install(self):
        if not super().install():
            return False
        libcrypt1 = None
        result, ldCache = CraftCore.cache.getCommandOutput("/usr/sbin/ldconfig", "-p")
        if result == 0:
            ldCache = ldCache.strip().splitlines()
            ldCachePattern = re.compile(r"^\s+(\S+)(?:\s.*)? => (\S+)")
            for line in ldCache:
                match = ldCachePattern.match(line)
                if match:
                    name, path = match.groups()
                    if name == "libcrypt.so.2":
                        # the system provides the lib
                        return True
                    if name == "libcrypt.so.1":
                        libcrypt1 = Path(path).resolve()
        if not libcrypt1:
            CraftCore.log.warning("Failed to locate libcrypt.so.1 or libcrypt.so.2")
            return False
        # create a copy, craft itself does not deploy symlinks pointing out of its root
        internalLibCrypt1 = self.installDir() / "lib" / libcrypt1.name
        return utils.copyFile(libcrypt1, internalLibCrypt1) and utils.createSymlink(
            internalLibCrypt1, self.installDir() / "lib/libcrypt.so.2", useAbsolutePath=True
        )
