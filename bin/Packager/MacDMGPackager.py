import contextlib
import glob
import io
import os
import stat
import subprocess
from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftBase import InitGuard
from CraftCore import CraftCore
from Packager.MacBasePackager import MacBasePackager
from Utils import CraftHash, CodeSign


class MacDMGPackager(MacBasePackager):

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        MacBasePackager.__init__(self, whitelists, blacklists)

    def setDefaults(self, defines: {str:str}) -> {str:str}:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.dmg"
        return defines

    def createPackage(self):
        """ create a package """
        CraftCore.log.debug("packaging using the MacDMGPackager")

        defines = self.setDefaults(self.defines)
        # TODO: provide an image with dbg files
        if not self.internalCreatePackage(defines):
            return False
        appPath = self.getMacAppPath(defines)
        if not appPath:
            return False
        archive = os.path.normpath(self.archiveDir())

        CraftCore.log.info(f"Packaging {appPath}")

        dmgDest = defines["setupname"]
        if os.path.exists(dmgDest):
            utils.deleteFile(dmgDest)
        appName = defines['appname'] + ".app"
        if not utils.system(["create-dmg", "--volname", os.path.basename(dmgDest),
                                # Add a drop link to /Applications:
                                "--icon", appName, "140", "150", "--app-drop-link", "350", "150",
                                dmgDest, appPath]):
            return False

        if not CodeSign.signMacPackage(dmgDest):
                return False
        CraftHash.createDigestFiles(dmgDest)

        return True
