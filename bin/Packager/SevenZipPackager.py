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
        PackagerBase.__init__(self)
        fileName = "bin\\7za.exe"
        self.packager = None
        for dir in [".","dev-utils", "release", "debug"]:
            path = os.path.join(self.rootdir, dir, fileName )
            if os.path.exists(path):
                self.packager = path
                break
        if not self.packager == None:
            utils.debug("using 7za from %s" % self.packager,2)

    def createPackage(self):
        """create 7z package with digest files located in the manifest subdir"""

        if not self.packager:
            utils.die("could not find 7za in your path!")

        if self.subinfo.options.package.packageName <> None:
            pkgName = self.subinfo.options.package.packageName
        else:
            pkgName = self.package
            
        if pkgName.endswith('-src') or pkgName.endswith('-pkg'):
            pkgName = pkgName[:-4]

        pkgVersion, pkgNotesVersion = self.getPackageVersion()

        if self.subinfo.options.package.withArchitecture:
            if self.buildArchitecture() == "x64": 
                pkgName += "-x64"
            else:
                pkgName += "-x86"

        if self.subinfo.options.package.packageFromSubDir:
            filesDir = os.path.join(self.imageDir(),self.subinfo.options.package.packageFromSubDir)
        else:
            filesDir = self.imageDir()
           
        if self.subinfo.options.package.withDigests:
            utils.createManifestFiles(filesDir, filesDir,"",self.package,pkgVersion)

        ## \todo do we have a wrapper for this ?
        destPath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not destPath:
            destPath = os.path.join( self.rootdir, "tmp" )

        if self.subinfo.options.package.withCompiler:
            if( self.compiler() == "mingw"):
              pkgCompiler = "-mingw"
            elif self.compiler() == "mingw4":
              pkgCompiler = "-mingw4 "
            elif self.compiler() == "msvc2005":
              pkgCompiler = "-msvc"
            elif self.compiler() == "msvc2008":
              pkgCompiler = "-vc90"
            elif self.compiler() == "msvc2010":
              pkgCompiler = "-vc100"
            else:
              pkgCompiler = "-unknown"
        else:
            pkgCompiler=""

        if self.subinfo.options.package.packageSuffix:
            pkgSuffix = self.subinfo.options.package.packageSuffix
        else:
            pkgSuffix = ''

        archiveName = "%s-%s%s%s.7z" % (self.package, pkgVersion, pkgCompiler, pkgSuffix)
        fileName = os.path.join(destPath,archiveName)
        utils.deleteFile(fileName)
        cmd = "cd %s && %s a -r %s %s" % (filesDir, self.packager, fileName, '*.*')
        utils.system( cmd ) or utils.die( "while packaging. cmd: %s" % cmd )

        if not self.subinfo.options.package.packSources:
            return True

        pkgSuffix = '-src'
        archiveName = "%s-%s%s%s.7z" % (self.package, pkgVersion, pkgCompiler, pkgSuffix)
        fileName = os.path.join(destPath,archiveName)
        utils.deleteFile(fileName)
        cmd = "cd %s && %s a -x!.svn -x!.git -r %s %s" % (self.sourceDir(), self.packager, fileName, '*.*')
        utils.system( cmd ) or utils.die( "while packaging. cmd: %s" % cmd )
        return True
