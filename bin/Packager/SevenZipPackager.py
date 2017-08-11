#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
# creates a 7z archive from the whole content of the package image
# directory or optional from a sub directory of the image directory

# This packager is in an experimental state - the implementation
# and features may change in further versions

import json

# TODO:
# - password support
# - self extraction archives
#
#
import CraftHash
from Packager.PackagerBase import *


class SevenZipPackager(PackagerBase):
    """Packager using the 7za command line tool from the dev-utils/7zip package"""

    @InitGuard.init_once
    def __init__(self):
        PackagerBase.__init__(self)

    def _compress(self, archiveName, sourceDir, destDir):
        utils.deleteFile(archiveName)
        app = utils.utilsCache.findApplication("7za")
        kw = {}
        progressFlags = ""
        if utils.utilsCache.checkCommandOutputFor(app, "-bs"):
            progressFlags = " -bso2 -bsp1"
            kw["stderr"] = subprocess.PIPE
        archive = os.path.join(destDir, archiveName)
        if os.path.isfile(archive):
            utils.deleteFile(archive)
        cmd = f"\"{app}\" a {progressFlags} -r \"{archive}\" \"{sourceDir}/*\""
        if not utils.system(cmd, displayProgress=True, **kw):
            craftDebug.log.critical(f"while packaging. cmd: {cmd}")
        if not craftSettings.getboolean("Packager", "CreateCache"):
            CraftHash.createDigestFiles(archive)
        else:
            cacheFilePath = os.path.join(self.cacheLocation(), "manifest.json")
            if os.path.exists(cacheFilePath):
                with open(cacheFilePath, "rt+") as cacheFile:
                    cache = json.load(cacheFile)
            else:
                cache = {}
            if not str(self) in cache:
                cache[str(self)] = {}
            cache[str(self)][archiveName] = {"checksum": CraftHash.digestFile(archive, CraftHash.HashAlgorithm.SHA256)}
            with open(cacheFilePath, "wt+") as cacheFile:
                json.dump(cache, cacheFile, sort_keys=True, indent=2)

    def createPackage(self):
        """create 7z package with digest files located in the manifest subdir"""
        cacheMode = craftSettings.getboolean("Packager", "CreateCache", False)
        if cacheMode:
            if self.subinfo.options.package.disableBinaryCache:
                return True
            dstpath = self.cacheLocation()
        else:
            dstpath = self.packageDestinationDir()

        self._compress(self.binaryArchiveName(includePackagePath=cacheMode), self.imageDir(), dstpath)
        if not self.subinfo.options.package.packSources:
            return True
        if craftSettings.getboolean("Packager", "PackageSrc", "True"):
            self._compress(self.binaryArchiveName("-src", includePackagePath=cacheMode), self.sourceDir(), dstpath)
        return True
