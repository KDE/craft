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
from Packager.PackagerBase import *

class SevenZipPackager (PackagerBase):
    """Packager using the 7za command line tool from the dev-utils/7zip package"""
    def __init__(self):
        PackagerBase.__init__( self )
        fileName = "bin\\7za.exe"
        self.packagerExe = None
        for directory in [".", "dev-utils", "release", "debug"]:
            path = os.path.join(self.rootdir, directory, fileName )
            if os.path.exists(path):
                self.packagerExe = path
                break
        if self.packagerExe:
            utils.debug("using 7za from %s" % self.packagerExe, 2)

    def _archiveName(self, pkgSuffix):
        pkgVersion, _ = self.getPackageVersion()
        if self.package.endswith( "-package" ):
            shortPackage = self.package[ : -8 ]
        else:
            shortPackage = self.package

        return "%s-%s-%s%s%s.%s" % (shortPackage, compiler.architecture(), pkgVersion, compiler.getShortName(), pkgSuffix, emergeSettings.get("Packager", "7ZipArchiveType"))

    def _compress(self, archiveName, sourceDir, destDir):
        utils.deleteFile(archiveName)
        cmd = "%s a -r %s %s/*" % (self.packagerExe, os.path.join(destDir, archiveName), sourceDir )
        if not utils.system(cmd):
            utils.die( "while packaging. cmd: %s" % cmd )

    def createPackage(self):
        """create 7z package with digest files located in the manifest subdir"""

        if not self.packagerExe:
            utils.die("could not find 7za in your path!")


        dstpath = self.packageDestinationDir()
        print(dstpath)

        pkgSuffix = ''
        if hasattr(self.subinfo.options.package, 'packageSuffix') and self.subinfo.options.package.packageSuffix:
            pkgSuffix = self.subinfo.options.package.packageSuffix


        self._compress(self._archiveName( pkgSuffix), self.imageDir(), dstpath)



        if not self.subinfo.options.package.packSources:
            return True

        self._compress(self._archiveName( "-src"), self.sourceDir(), dstpath)
        return True
