import os

import utils
from CraftBase import InitGuard
from CraftCore import CraftCore
from Packager.MacBasePackager import MacBasePackager
from Utils import CodeSign, CraftHash


class MacDMGPackager(MacBasePackager):
    @InitGuard.init_once
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setDefaults(self, defines: set[str, str]) -> set[str, str]:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.dmg"
        return defines

    def createPackage(self):
        """create a package"""
        CraftCore.log.debug("packaging using the MacDMGPackager")

        defines = self.setDefaults(self.defines)
        # TODO: provide an image with dbg files
        if not self.internalCreatePackage(defines):
            return False
        appPath = self.getMacAppPath(defines)
        if not appPath:
            return False

        CraftCore.log.info(f"Packaging {appPath}")

        dmgDest = defines["setupname"]
        if os.path.exists(dmgDest):
            utils.deleteFile(dmgDest)
        appName = defines["appname"] + ".app"
        if not utils.system(
            [
                "create-dmg",
                "--volname",
                os.path.basename(dmgDest),
                # Add a drop link to /Applications:
                "--icon",
                appName,
                "140",
                "150",
                "--app-drop-link",
                "350",
                "150",
                dmgDest,
                appPath,
            ]
        ):
            return False

        if not CodeSign.signMacPackage(dmgDest):
            return False
        CraftHash.createDigestFiles(dmgDest)

        return True
