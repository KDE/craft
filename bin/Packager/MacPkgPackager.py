import os
from pathlib import Path

import utils
from CraftBase import InitGuard
from CraftCore import CraftCore
from Packager.MacBasePackager import MacBasePackager
from Packager.PackagerBase import DefinesDict
from Utils import CodeSign, CraftHash


class MacPkgPackager(MacBasePackager):
    @InitGuard.init_once
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setDefaults(self, defines: DefinesDict) -> DefinesDict:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.pkg"
        return defines

    def createPackage(self):
        """create a package"""
        CraftCore.log.debug("packaging using the MacDMGPackager")
        if not CraftCore.cache.findApplication("packagesutil"):
            CraftCore.log.critical(
                "Craft requires dev-utils/packagesdev to create a package, please install dev-utils/packagesdev\n" "\t'craft dev-utils/packagesdev'"
            )
            return False

        defines = self.setDefaults(self.defines)
        if "pkgproj" not in defines:
            CraftCore.log.error("Cannot not create .pkg because no .pkgproj was defined.")
            return False
        if not self.internalCreatePackage(defines):
            return False

        packageDest = Path(defines["setupname"])
        if packageDest.exists():
            utils.deleteFile(packageDest)

        pkgprojPath = defines["pkgproj"]
        # set output file basename
        packagesutil = CraftCore.cache.findApplication("packagesutil")
        if not utils.system(
            [
                packagesutil,
                "--file",
                pkgprojPath,
                "set",
                "project",
                "name",
                packageDest.stem,
            ]
        ):
            return False

        packagesbuild = CraftCore.cache.findApplication("packagesbuild")
        if not utils.system(
            [
                packagesbuild,
                "-v",
                "--reference-folder",
                os.path.dirname(self.getMacAppPath(defines)),
                "--build-folder",
                packageDest.parent,
                pkgprojPath,
            ]
        ):
            return False

        if not CodeSign.signMacPackage(packageDest):
            return False

        CraftHash.createDigestFiles(packageDest)

        return True
