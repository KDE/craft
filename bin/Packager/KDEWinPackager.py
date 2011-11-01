#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

from Packager.PackagerBase import *
import compiler
import subprocess

class KDEWinPackager (PackagerBase):
    """Packager for KDEWin installer"""
    def __init__(self):
        PackagerBase.__init__( self )
        fileName = "bin\\kdewin-packager.exe"
        self.packagerExe = None
        self.useDebugPackages = False
        for directory in [".", "dev-utils", "release", "debug"]:
            path = os.path.join(self.rootdir, directory, fileName )
            if os.path.exists(path):
                self.packagerExe = path
                break
        if self.packagerExe:
            utils.debug("using kdewin packager from %s" % self.packagerExe, 2)
            tmp = subprocess.Popen(self.packagerExe, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            self.useDebugPackages = any("symroot" in line for line in tmp)

    def xmlTemplate(self):
        template = os.path.join(self.packageDir(), self.package+"-package.xml")
        if not os.path.exists(template):
            template = os.path.join(self.packageDir(), self.package+".xml")
        return template

    ## \todo rename to package()
    def createPackage(self):
        """packaging according to the gnuwin32 packaging rules.
        This requires the kdewin-packager"""

        if not self.packagerExe:
            utils.die("could not find kdewin-packager in your path!")

        if self.subinfo.options.package.packageName != None:
            pkgName = self.subinfo.options.package.packageName
        else:
            pkgName = self.package

        if pkgName.endswith('-src') or pkgName.endswith('-pkg'):
            pkgName = pkgName[:-4]

        pkgVersion, pkgNotesVersion = self.getPackageVersion()

        # kdewin packager creates his own manifest files, so there is no need to add
        # if self.subinfo.options.package.withDigests:
        #    utils.createManifestFiles(filesDir, filesDir, "", self.package, pkgVersion)

        # FIXME: add a test for the installer later
        dstpath = self.packageDestinationDir()

        for pkgtype in ['bin', 'lib', 'doc', 'src', 'dbg']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, pkgVersion, pkgtype )
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if os.path.exists( script ):
                if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                    os.mkdir( os.path.join( self.imageDir(), "manifest" ) )
                utils.copyFile( script, destscript )

        if ( self.subinfo.options.package.packSources ) and os.path.exists( self.sourceDir() ):
            srcCmd = " -srcroot " + self.sourceDir()
        else:
            if not os.path.exists( self.sourceDir() ):
                utils.warning( "The source directory %s doesn't exist and can't be used for packaging." % self.sourceDir() )
            srcCmd = ""

        # copy pdb/sym files to a temporary directory, because they can be scattered all over the build directory
        # plus, different build types copy files to different directories (could be buildDir(), buildDir()/bin, buildDir()/bin/Debug...),
        # so let's copy them to one precise location, package them, then delete that directory

        symCmd = ""
        if self.useDebugPackages:
            # directories to ignore: cmake temporary files, and dbg so it won't try to copy a file to itself
            dirsToIgnore = [ 'cmake', 'CMakeFiles', 'CMakeTmp', 'CMakeTmp2', 'CMakeTmp3', 'dbg' ]
            path = self.buildDir()
            # where to copy the debugging information files
            symRoot = os.path.join( self.buildDir(), "dbg" )
            symPath = os.path.join( symRoot, "bin" )
            if not os.path.exists( symPath ):
                utils.createDir( symPath )
            # shouldn't be needed, usually; but if files are present, that could lead to errors
            utils.cleanDirectory ( symRoot )

            utils.debug( "Copying debugging files to 'dbg'..." )
            for path, _, files in os.walk( path ):
                found = 0
                for directory in range( 0, len( dirsToIgnore ) ):
                    if path.find( dirsToIgnore[directory] ) > 0:
                        found = 1
                        break
                if found == 1:
                    continue
                utils.debug( "Checking: %s" % path, 3 )
                for fileName in files:
                    if ( fileName.endswith( ".pdb" ) ):
                        utils.copyFile( os.path.join( path, fileName ), os.path.join( symPath, fileName ) )
                    elif not self.subinfo.options.package.disableStriping:
                        if ( fileName.endswith( ".exe" ) or fileName.endswith( ".dll" ) ):
                            if compiler.isMinGW():
                                symFilename = fileName[:-4] + ".sym"
                                utils.system( "strip --only-keep-debug " + " -o " + os.path.join( path, symFilename ) \
                                        + " " + os.path.join( path, fileName ) )
                                # utils.system( "strip --strip-all " + os.path.join( path, fileName ) )
                                utils.copyFile( os.path.join(path, symFilename), os.path.join( symPath, symFilename ) )

            if not self.subinfo.options.package.disableStriping and compiler.isMinGW() :
                symCmd += "-strip "
            symCmd += "-debug-package "
            symCmd += "-symroot " + symRoot
            utils.debug ( symCmd, 2 )

        cmd = "-name %s -root %s -version %s -destdir %s %s %s -checksum sha1 " % \
                  ( pkgName, self.imageDir(), pkgVersion, dstpath, srcCmd, symCmd )
        xmltemplate = self.xmlTemplate()
        if os.path.exists(xmltemplate):
            cmd = self.packagerExe + " " + cmd + " -template " + xmltemplate + " -notes " + \
                    "%s/%s:%s:unknown " % ( self.category, self.package, pkgNotesVersion ) + "-compression 2 "
            utils.debug("using xml template for package generating", 1)
        elif self.package == "qt":
            cmd = self.packagerExe + " " + cmd + " -template :/template-qt.xml -notes " + \
                    "%s/%s:%s:unknown " % ( self.category, self.package, pkgNotesVersion ) + "-compression 2 "
            utils.debug("using xml template for package generating", 1)
        else:
            cmd = self.packagerExe + " " + cmd + " -verbose -notes " + \
                    "%s/%s:%s:unknown " % ( self.category, self.package, pkgNotesVersion ) + "-compression 2 "
            utils.debug(" xml template %s for package generating not found" % xmltemplate, 1)

        if( self.subinfo.options.package.withCompiler ):
            if( self.compiler() == "mingw"):
                cmd += " -type mingw "
            elif self.compiler() == "mingw4" and self.buildArchitecture() == "x64":
                cmd += " -type x64-mingw4 "
            elif self.compiler() == "mingw4" and compiler.isMinGW_W32():
                cmd += " -type x86-mingw4 "
            elif self.compiler() == "mingw4":
                cmd += " -type mingw4 "
            elif self.compiler() == "msvc2005":
                cmd += " -type msvc "
            elif self.compiler() == "msvc2008":
                cmd += " -type vc90 "
            elif self.compiler() == "msvc2010":
                cmd += " -type vc100 "
            else:
                cmd += " -type unknown "


#        not needed anymore
#        if self.subinfo.options.package.specialMode:
#            cmd += " -special"

        if not utils.system(cmd):
            utils.die( "while packaging. cmd: %s" % cmd )

        if self.useDebugPackages:
            utils.rmtree( symPath )
        return True
