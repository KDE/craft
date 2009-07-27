# -*- coding: utf-8 -*-
# Packager base

from Packager.PackagerBase import *

class KDEWinPackager (PackagerBase):
    """Packager for KDEWin installer"""
    def __init__(self):
        PackagerBase.__init__(self)

    def createPackage(self):
        """packaging according to the gnuwin32 packaging rules"""
        """this requires the kdewin-packager"""
        pkg_name = self.package
        pkg_version = str( datetime.date.today() ).replace('-', '')
        packSources = True 
        special = False 
    
        # FIXME: add a test for the installer later
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )
         
        if not utils.test4application( "kdewin-packager" ):
            utils.die( "kdewin-packager not found - please make sure it is in your path" )

        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if os.path.exists( script ):
                if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                    os.mkdir( os.path.join( self.imageDir(), "manifest" ) )
                shutil.copyfile( script, destscript )
        
        # todo: this is probably code for dealing with svn repositories 
        # need to be refactored
        if ( packSources ):
            srcCmd = " -srcroot " + self.source.sourceDir()
        else:
            srcCmd = ""
            
        cmd = "-name %s -root %s -version %s -destdir %s %s" % \
                  ( pkg_name, self.installDir(), pkg_version, dstpath, srcCmd )
        xmltemplate=os.path.join(self.packageDir(),pkg_name+"-package.xml")
        if os.path.exists(xmltemplate):
            cmd = "kdewin-packager.exe " + cmd + " -template " + xmltemplate + " -notes " + "%s/%s:%s:unknown " % ( self.category, self.package, self.version ) + "-compression 2 "
        else:
            cmd = "kdewin-packager.exe " + cmd + " -notes " + "%s/%s:%s:unknown " % ( self.category, self.package, self.version ) + "-compression 2 "
        
        if( not self.createCombinedPackage ):
            if( self.compiler() == "mingw"):
              cmd += " -type mingw "
            elif self.compiler() == "msvc2005":
              cmd += " -type msvc "
            elif self.compiler() == "msvc2008":
              cmd += " -type vc90 "
            else:
              cmd += " -type unknown "

        if special:
            cmd += " -special"

        utils.system( cmd ) or utils.die( "while packaging. cmd: %s" % cmd )
        return True




