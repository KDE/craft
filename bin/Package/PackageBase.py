
from EmergeBase import *;
import os;
import utils;

class PackageBase (EmergeBase):
    """
     provides a generic interface for packages and implements the basic stuff for all
     packages
    """

    # uses the following instance variables 
    # todo: place in related ...Base
    
    #rootdir    -> EmergeBase  
    #package    -> PackageBase
    #force      -> PackageBase
    #category   -> PackageBase
    #version    -> PackageBase
    #packagedir -> PackageBase
    #imagedir   -> PackageBase
    
    def __init__(self):
        if utils.verbose > 1:
            print "PackageBase.__init__ called"
        EmergeBase.__init__(self)

    def qmerge( self ):
        """mergeing the imagedirectory into the filesystem"""
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packagedir, "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                os.mkdir( os.path.join( self.imageDir(), "manifest" ) )
            if os.path.exists( script ):
                shutil.copyfile( script, destscript )

        utils.mergeImageDirToRootDir( self.imageDir(), self.mergeDir() )

        # run post-install scripts
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            script = os.path.join( self.rootdir, "manifest", scriptName )
            if os.path.exists( script ):
                cmd = "cd %s && %s" % ( self.rootdir, script )
                utils.system( cmd ) or utils.warning("%s failed!" % cmd )
        utils.addInstalled( self.category, self.package, self.version )
        return True

    def unmerge( self ):
        """unmergeing the files from the filesystem"""
        if utils.verbose() > 1:
            print "base unmerge called"

        utils.unmerge( self.mergeDir(), self.package, self.forced )
        utils.remInstalled( self.category, self.package, self.version )
        return True

    def cleanup( self ):
        """cleanup before install to imagedir"""
        if hasattr(self,'buildSystemType') and self.buildSystemType == 'binary' or hasattr(self,'buildsystem') and self.buildsystem.buildSystemType == 'binary':
            utils.debug("skipped cleaning image dir because we use binary build system",1)
            return True
        if ( os.path.exists( self.imageDir() ) ):
            utils.debug( "cleaning image dir: %s" % self.imageDir(), 1 )
            utils.cleanDirectory( self.imageDir() )
        return True
        
    def manifest( self ):
        """installer compatibility: make the manifest files that make up the installers"""
        """install database"""
        print "manifest should be created on qmerge "
    
        if utils.verbose() > 1:
            print "base manifest called"
        utils.manifestDir( os.path.join( self.workDir(), self.instsrcdir, self.package ), self.imageDir(), self.category, self.package, self.version )
        return True

 
