# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

from Packager.PackagerBase import *

class KDEWinPackager (PackagerBase):
    """Packager for KDEWin installer"""
    def __init__(self):
        PackagerBase.__init__(self)
        fileName = "bin\\kdewin-packager.exe"
        self.packager = None
        for dir in [".","dev-utils", "release", "debug"]:
            path = os.path.join(self.rootdir, dir, fileName )
            if os.path.exists(path):
                self.packager = path
                break
        if not self.packager == None:
            utils.debug("using kdewin packager from %s" % self.packager,2)
            
    def xmlTemplate(self):
        template = os.path.join(self.packageDir(),self.package+"-package.xml")
        if not os.path.exists(template):
            template = os.path.join(self.packageDir(),self.package+".xml")
        return template

    ## \todo rename to package()
    def createPackage(self):
        """packaging according to the gnuwin32 packaging rules"""
        """this requires the kdewin-packager"""

        if not self.packager:
            utils.die("could not find kdewin-packager in your path!")

        if self.subinfo.options.package.packageName <> None:
            pkgName = self.subinfo.options.package.packageName
        else:
            pkgName = self.package
            
        if pkgName.endswith('-src') or pkgName.endswith('-pkg'):
            pkgName = pkgName[:-4]

        if self.subinfo.options.package.version <> None:
            pkgVersion = self.subinfo.options.package.version
            pkgNotesVersion = pkgVersion
        elif self.subinfo.buildTarget == "gitHEAD" or self.subinfo.buildTarget == "svnHEAD":
            pkgVersion = str( datetime.date.today() ).replace('-', '')
            pkgNotesVersion = pkgVersion
        else: 
            pkgVersion = self.subinfo.buildTarget
            pkgNotesVersion = pkgVersion

        if "EMERGE_PKGPATCHLVL" in os.environ:
            pkgVersion += "-" + os.environ["EMERGE_PKGPATCHLVL"]

        if self.buildArchitecture() == "x64": 
            pkgName += "-x64"
        #else:
        #    pkgName += "-x86"
            
        # FIXME: add a test for the installer later
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )
         
        for pkgtype in ['bin', 'lib', 'doc', 'src', 'dbg']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, pkgVersion, pkgtype )
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if os.path.exists( script ):
                if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                    os.mkdir( os.path.join( self.imageDir(), "manifest" ) )
                utils.copyFile( script, destscript )
        
        sourcedir = self.sourceDir()
        
        # todo: this is probably code for dealing with svn repositories 
        # need to be refactored
        if ( self.subinfo.options.package.packSources ):
            srcCmd = " -srcroot " + sourcedir
        else:
            srcCmd = ""
            
        symCmd = "-debug-package "
        symCmd += "-symroot " + os.path.join( self.buildDir(), "bin" )
        utils.debug ( symCmd )
            
        cmd = "-name %s -root %s -version %s -destdir %s %s %s -checksum sha1 " % \
                  ( pkgName, self.installDir(), pkgVersion, dstpath, srcCmd, symCmd )
        xmltemplate=self.xmlTemplate()
        if os.path.exists(xmltemplate):
            cmd = self.packager + " " + cmd + " -template " + xmltemplate + " -notes " + "%s/%s:%s:unknown " % ( self.category, self.package, pkgNotesVersion ) + "-compression 2 "
            utils.debug("using xml template for package generating",1) 
        else:
            cmd = self.packager + " " + cmd + " -notes " + "%s/%s:%s:unknown " % ( self.category, self.package, pkgNotesVersion ) + "-compression 1 "
            utils.debug(" xml template %s for package generating not found" % xmltemplate,1) 
        
        if( self.subinfo.options.package.withCompiler ):
            if( self.compiler() == "mingw"):
              cmd += " -type mingw "
            elif self.compiler() == "mingw4":
              cmd += " -type mingw4 "
            elif self.compiler() == "msvc2005":
              cmd += " -type msvc "
            elif self.compiler() == "msvc2008":
              cmd += " -type vc90 "
            else:
              cmd += " -type unknown "

            
        if self.subinfo.options.package.specialMode:
            cmd += " -special"

        utils.system( cmd ) or utils.die( "while packaging. cmd: %s" % cmd )
        return True




