# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        # It is called liblzma, but in reality we are shiping xz utils, because:
        # Users of LZMA Utils should move to XZ Utils. XZ Utils support the legacy .lzma format used by LZMA Utils,
        # and can also emulate the command line tools of LZMA Utils.
        self.description = "free general-purpose data compression software with high compression ratio"
        self.webpage = "https://tukaani.org/xz"
        self.releaseManagerId = 5277

        for ver in ["5.8.4"]:
            self.targets[ver] = f"https://github.com/tukaani-project/xz/releases/download/v{ver}/xz-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"xz-{ver}"

        self.targetDigests["5.8.4"] = (["4ce24038fd4221e0d13bc1a2de7a4db56e90b92b3bf75321f6c14be73f65de4b"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "5.8.4"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
