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
import EmergeDebug
from Packager.PackagerBase import *

class SevenZipPackager (PackagerBase):
    """Packager using the 7za command line tool from the dev-utils/7zip package"""
    def __init__( self, initialized = False ):
        if not initialized: PackagerBase.__init__( self )
        self.packagerExe = utils.UtilsCache.findApplication("7za")

    def _compress(self, archiveName, sourceDir, destDir):
        utils.deleteFile(archiveName)
        cmd = "%s a -r %s %s/*" % (self.packagerExe, os.path.join(destDir, archiveName), sourceDir )
        cmd += " -bsp1"
        if EmergeDebug.verbose() <= 1:
            cmd += " -bso0"
        if not utils.system(cmd):
            EmergeDebug.die("while packaging. cmd: %s" % cmd)

    def createPackage(self):
        """create 7z package with digest files located in the manifest subdir"""

        if not self.packagerExe:
            EmergeDebug.die("could not find 7za in your path!")

        if emergeSettings.get("ContinuousIntegration", "Cache"):
            dstpath = os.path.join(EmergeStandardDirs.downloadDir(), "binary")
        else:
            dstpath = self.packageDestinationDir()
        self._compress(self.binaryArchiveName(), self.imageDir(), dstpath)
        if not self.subinfo.options.package.packSources:
            return True

        self._compress(self.binaryArchiveName("-src"), self.sourceDir(), dstpath)
        return True
