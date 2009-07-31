
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
        utils.debug("PackageBase.__init__ called",2)
        EmergeBase.__init__(self)
        self.forceCreateManifestFiles = False

    def __installedDBPrefix(self):
        if self.useBuildTypeRelatedMergeRoot:
            if self.buildType() == 'Debug':
                postfix = 'debug'
            elif self.buildType() == 'Release':
                postfix =  'release'
        else:
            postfix =  ''
        return postfix

    def qmerge( self ):
        """mergeing the imagedirectory into the filesystem"""
 
        ## \todo is this the optimal place for creating the post install scripts ? 
        # create post install scripts 
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            # are there any cases there installDir should be honored ? 
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                os.mkdir( os.path.join( self.imageDir(), "manifest" ) )
            if os.path.exists( script ):
                shutil.copyfile( script, destscript )

        utils.mergeImageDirToRootDir( self.mergeSourceDir(), self.mergeDestinationDir() )
        self.manifest()

        # run post-install scripts
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            script = os.path.join( self.rootdir, "manifest", scriptName )
            if os.path.exists( script ):
                cmd = "cd %s && %s" % ( self.rootdir, script )
                utils.system( cmd ) or utils.warning("%s failed!" % cmd )

        # add package to installed database -> is this not the task of the manifest files ? 
       
        utils.addInstalled( self.category, self.package, self.version, self.__installedDBPrefix() )
        return True

    def unmerge( self ):
        """unmergeing the files from the filesystem"""
        utils.debug("base unmerge called",2)

        ## \todo mergeDestinationDir() reads the real used merge dir from the 
        ## package definition, which fails if this is changed 
        ## a better solution will be to save the merge sub dir into 
        ## /etc/portage/installed and to read from it on unmerge
        utils.unmerge( self.mergeDestinationDir(), self.package, self.forced )
        utils.remInstalled( self.category, self.package, self.version, self.__installedDBPrefix() )
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
    
        utils.debug("base manifest called",2)
        if not utils.hasManifestFile( self.mergeDestinationDir(), self.category, self.package ) or self.forceCreateManifestFiles:
            utils.debug("creating of manifest files triggered", 1)
            utils.createManifestFiles( self.mergeSourceDir(), self.mergeDestinationDir(), self.category, self.package, self.version )
        return True

 
