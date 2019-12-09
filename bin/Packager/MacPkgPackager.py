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
from Utils import CraftHash

class MacPkgPackager( MacBasePackager ):

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        MacBasePackager.__init__(self, whitelists, blacklists)

    def setDefaults(self, defines: {str:str}) -> {str:str}:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.pkg"
        return defines

    def createPackage(self):
        """ create a package """
        CraftCore.log.debug("packaging using the MacDMGPackager")

        defines = self.setDefaults(self.defines)
        if not "pkgproj" in defines:
            CraftCore.log.error("Cannot not create .pkg because no .pkgproj was defined.")
            return False
        # TODO: provide an image with dbg files
        if not self.internalCreatePackage(defines):
            return False

        packageDest = defines["setupname"]
        if os.path.exists(packageDest):
            utils.deleteFile(packageDest)

        pkgprojPath = defines["pkgproj"]
        # set output file basename
        packagesutil = CraftCore.cache.findApplication("packagesutil")
        if not utils.system([packagesutil, '--file', pkgprojPath, 'set', 'project', 'name', defines["display_name"]]):
            return False

        packagesbuild = CraftCore.cache.findApplication("packagesbuild")
        if not utils.system([packagesbuild, '--reference-folder', os.path.join(self.archiveDir(), 'bin'), '--build-folder', self.packageDestinationDir(), pkgprojPath]):
            return False

        if not utils.signMacPackage(packageDest):
            return False

        CraftHash.createDigestFiles(packageDest)

        return True
