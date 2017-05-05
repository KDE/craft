#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
# creates a 7z archive from the whole content of the package image
# directory or optional from a sub directory of the image directory

# This packager is in an experimental state - the implementation
# and features may change in further versions

# TODO:
# - password support
# - self extraction archives
#
#
from CraftDebug import craftDebug
import CraftHash
from Packager.PackagerBase import *

class SevenZipPackager (PackagerBase):
    """Packager using the 7za command line tool from the dev-utils/7zip package"""
    def __init__( self, initialized = False ):
        if not initialized: PackagerBase.__init__( self )

    def _compress(self, archiveName, sourceDir, destDir):
        utils.deleteFile(archiveName)
        app = utils.utilsCache.findApplication("7za")
        kw = {}
        progressFlags = ""
        if utils.utilsCache.appSupportsCommand(app, "-bs"):
            progressFlags = " -bso2 -bsp1"
            kw["stderr"] = subprocess.PIPE
        archive = os.path.join(destDir, archiveName)
        cmd = f"\"{app}\" a {progressFlags} -r \"{archive}\" \"{sourceDir}/*\""
        if not utils.system(cmd, displayProgress=True, **kw):
            craftDebug.log.critical(f"while packaging. cmd: {cmd}")
        CraftHash.createDigestFiles(os.path.join(destDir, archiveName))

    def createPackage(self):
        """create 7z package with digest files located in the manifest subdir"""
        if craftSettings.getboolean("Packager", "CreateCache"):
            if self.subinfo.options.package.disableBinaryCache:
                return True
            dstpath = self.cacheLocation()
        else:
            dstpath = self.packageDestinationDir()

        self._compress(self.binaryArchiveName(), self.imageDir(), dstpath)
        if not self.subinfo.options.package.packSources:
            return True
        if craftSettings.getboolean("Packager", "PackageSrc", "True"):
            self._compress(self.binaryArchiveName("-src"), self.sourceDir(), dstpath)
        return True

