
from EmergeBase import *;
import os;
import shutils;
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
    #forced      -> for what this this variable good ? 
    #category   -> PackageBase
    #version    -> PackageBase
    #workdir    -> PackageBase
    #packagedir -> PackageBase
    #imagedir   -> PackageBase
    
	def __init__(self):
		EmergeBase.__init__(self)
	
    def qmerge( self ):
        """mergeing the imagedirectory into the filesystem"""
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packagedir, "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            destscript = os.path.join( self.imagedir, "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imagedir, "manifest" ) ):
                os.mkdir( os.path.join( self.imagedir, "manifest" ) )
            if os.path.exists( script ):
                shutil.copyfile( script, destscript )
                             
        utils.mergeImageDirToRootDir( self.imagedir, self.rootdir )

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
        utils.unmerge( self.rootdir, self.package, self.forced )
        utils.remInstalled( self.category, self.package, self.version )
        return True

    def setup(self):
		"""
		 

		@return  :
		@author
		"""
		pass

	def clean(self):
		"""
		 

		@return  :
		@author
		"""
		pass
