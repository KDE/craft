#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
# creates a 7z archive from the whole content of the package image
# directory or optional from a sub directory of the image directory

# This packager is in an experimental state - the implementation
# and features may change in further versions

import json
import subprocess

from Packager.PackagerBase import *
# TODO:
# - password support
# - self extraction archives
#
#
from Utils import CraftHash


class SevenZipPackager(PackagerBase):
    """Packager using the 7za command line tool from the dev-utils/7zip package"""

    @InitGuard.init_once
    def __init__(self):
        PackagerBase.__init__(self)

    def _compress(self, archiveName, sourceDir, destDir):
        utils.deleteFile(archiveName)
        app = CraftCore.cache.findApplication("7za")
        kw = {}
        progressFlags = ""
        if CraftCore.cache.checkCommandOutputFor(app, "-bs"):
            progressFlags = " -bso2 -bsp1"
            kw["stderr"] = subprocess.PIPE
        archive = os.path.join(destDir, archiveName)
        if os.path.isfile(archive):
            utils.deleteFile(archive)
        cmd = f"\"{app}\" a {progressFlags} -r \"{archive}\" \"{sourceDir}/*\""
        if not utils.system(cmd, displayProgress=True, **kw):
            CraftCore.log.critical(f"while packaging. cmd: {cmd}")
        if not CraftCore.settings.getboolean("Packager", "CreateCache"):
            CraftHash.createDigestFiles(archive)
        else:
            self._generateManifest(destDir, archiveName, manifestLocation=self.cacheLocation())

    def createPackage(self):
        """create 7z package with digest files located in the manifest subdir"""
        cacheMode = CraftCore.settings.getboolean("Packager", "CreateCache", False)
        if cacheMode:
            if self.subinfo.options.package.disableBinaryCache:
                return True
            dstpath = self.cacheLocation()
        else:
            dstpath = self.packageDestinationDir()

        self._compress(self.binaryArchiveName(includePackagePath=cacheMode), self.imageDir(), dstpath)
        if not self.subinfo.options.package.packSources:
            return True
        if CraftCore.settings.getboolean("Packager", "PackageSrc", "True"):
            self._compress(self.binaryArchiveName("-src", includePackagePath=cacheMode), self.sourceDir(), dstpath)
        return True
