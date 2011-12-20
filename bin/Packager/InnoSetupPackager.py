#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

from Packager.PackagerBase import *

class InnoSetupPackager (PackagerBase):
    """Packager for Inno Setup installations"""
    def __init__(self):
        PackagerBase.__init__( self )
        self.packagerExe = os.path.join(os.environ["ProgramFiles"], "Inno Setup 5", "ISCC.exe")
        if self.packagerExe:
            utils.debug("using inno setup packager from %s" % self.packagerExe, 2)

    def configFile(self):
        """ return path of installer config file"""
        utils.debug("searching package dir for setup config", 2)

        fileName = os.path.join(self.buildDir(), "setup.iss")
        utils.debug("searching build dir for setup config %s" % fileName, 2)
        if os.path.exists(fileName):
            return fileName

        fileName = os.path.join(self.packageDir(), "setup.iss")
        if os.path.exists(fileName):
            return fileName

        fileName = os.path.join(self.packageDir(), "installer-config.iss")
        if os.path.exists(fileName):
            return fileName
        return None

    ## \todo rename to package()
    def createPackage(self):
        """packaging """
        print("createPackage from innosetupPackager")

        if not self.packagerExe:
            utils.die("could not find packager in your path!")

        if self.subinfo.options.package.packageName != None:
            pkgName = self.subinfo.options.package.packageName
        else:
            pkgName = self.package

        if pkgName.endswith('-src'):
            pkgName = pkgName[:-4]

        pkgVersion, _ = self.getPackageVersion()

        # perform variable substitution
        # variablenames are wrapped with '#..#' to not get
        # in conflict with cmake or other config file patching tools
        replacementPatterns = []
        replacementPatterns.append(["#EMERGE_PACKAGE_VERSION#", pkgVersion])
        replacementPatterns.append(["#EMERGE_INSTALL_DIR#", self.installDir()])
        replacementPatterns.append(["#EMERGE_MERGE_DESTINATION_DIR#", self.mergeDestinationDir()])

        if self.buildArchitecture() == "x64":
            pkgName += "-x64"
        #else:
        #    pkgName += "-x86"

        # FIXME: add a test for the installer later

        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, pkgVersion, pkgtype )
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if os.path.exists( script ):
                if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                    os.mkdir( os.path.join( self.imageDir(), "manifest" ) )
                utils.copyFile( script, destscript )

        # todo: this is probably code for dealing with svn repositories
        # needs to be refactored
        # determine source in case MultiSource is used
        #if hasattr(self,'source'):
        #    sourcedir = self.source.sourceDir()
        #elif hasattr(self.parent,'source'):
        #    sourcedir = self.parent.source.sourceDir()
        #else:
        #    sourcedir = self.sourceDir()

        #if ( self.subinfo.options.package.packSources ):
        #    srcCmd = " -srcroot " + sourcedir
        #else:
        #    srcCmd = ""

        if( self.subinfo.options.package.withCompiler ):
            if( self.compiler() == "mingw"):
                pkgName += "-mingw"
            elif self.compiler() == "mingw4":
                pkgName += "-mingw4"
            elif self.compiler() == "msvc2005":
                pkgName += "-msvc"
            elif self.compiler() == "msvc2008":
                pkgName += "-vc90"
            elif self.compiler() == "msvc2010":
                pkgName += "-vc100"
            else:
                pkgName += "-unknown "

        if self.subinfo.options.package.withDigests:
            if self.subinfo.options.package.packageFromSubDir:
                filesDir = os.path.join(self.imageDir(), self.subinfo.options.package.packageFromSubDir)
            else:
                filesDir = self.imageDir()
            utils.createManifestFiles(filesDir, filesDir, "", self.package, pkgVersion)

        dstpath = self.packageDestinationDir()

        cmd = "\"%s\" /O\"%s\" /F\"setup-%s-%s\"" % (self.packagerExe, dstpath, pkgName, pkgVersion)

        #
        # create config file from config File
        #
        infile = self.configFile()
        if infile == None:
            utils.die("could not find config file %s" % infile)
        with open(infile,'r') as _in:
            lines = _in.read().splitlines()

        outfile = os.path.join(self.buildDir(), "temp.iss")
        with open(outfile,'w') as out:
            for line in lines:
                a = line
                for pattern in replacementPatterns:
                    search = pattern[0]
                    if a.find(search) > -1:
                        a = line.replace(search, pattern[1])
                out.write(a + "\n")

        cmd += " \"%s\"" % (outfile)
        if not utils.systemWithoutShell(cmd):
            utils.die( "while packaging. cmd: %s" % cmd )
        return True



