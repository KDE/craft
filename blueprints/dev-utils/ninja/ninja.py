# -*- coding: utf-8 -*-

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # don't build and install gmock
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        """ """
        self.svnTargets["master"] = "https://github.com/martine/ninja.git"

        for ver in ["1.10.0", "1.10.2", "1.11.0", "1.11.1", "1.12.0", "1.12.1"]:
            self.targets[ver] = f"https://github.com/ninja-build/ninja/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"ninja-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ninja-{ver}"
            if CraftCore.compiler.platform.isMacOS:
                self.targetInstallPath[ver] = "dev-utils/ninja"
            else:
                self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["1.10.0"] = (
            ["3810318b08489435f8efc19c05525e80a993af5a55baa0dfeae0465a9d45f99f"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.10.2"] = (
            ["ce35865411f0490368a8fc383f29071de6690cbadc27704734978221f25e2bed"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.11.1"] = (
            ["31747ae633213f1eda3842686f83c2aa1412e0f5691d1c14dbbcc67fe7400cea"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.12.0"] = (
            ["8b2c86cd483dc7fcb7975c5ec7329135d210099a89bc7db0590a07b0bbfe49a5"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.patchToApply["1.10.0"] = [("34d1bf2f1dcc138f7cb3a54daf771931cd799785.patch", 1)]
        self.patchLevel["1.10.0"] = 1
        self.patchLevel["1.11.1"] = 3
        self.patchLevel["1.12.1"] = 1

        self.defaultTarget = "1.12.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/mingw-w64"] = None
        self.buildDependencies["dev-utils/cmake"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # building ninja with jom is broken
        self.subinfo.options.make.supportsMultijob = not CraftCore.compiler.platform.isWindows
        if CraftCore.compiler.platform.isMacOS:
            self.subinfo.options.configure.args += ["-DCMAKE_OSX_ARCHITECTURES=arm64;x86_64"]

    def postInstall(self):
        if not CraftCore.compiler.platform.isMacOS:
            return True
        # call ninja through arch to ensure a complete arch switch
        return utils.createShim(
            CraftCore.standardDirs.craftRoot() / "dev-utils/bin/ninja",
            "arch",
            useAbsolutePath=True,
            args=["-arch", CraftCore.compiler.hostArchitecture.name.lower(), str(CraftCore.standardDirs.craftRoot() / "dev-utils/ninja/bin/ninja")],
        )
