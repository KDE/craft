# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# subversion support
## \todo needs dev-utils/subversion package, add some kind of tool requirement tracking for SourceBase derived classes 

from VersionSystemSourceBase import *
import os
import utils

class SvnSource (VersionSystemSourceBase):
    """subversion support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)
        ## \todo add internal dependency for subversion package
        self.svnInstallDir = os.path.join(self.rootdir,'dev-utils','svn','bin')
        if not os.path.exists(self.svnInstallDir):
            utils.die("required subversion package not installed")
        
    def fetch( self ):
        """ checkout or update an existing repository path """
        if self.noFetch:
            utils.debug( "skipping svn fetch (--offline)" )
            return True

        for i in range(0, self.repositoryPathCount()):
            url = self.repositoryPath(i)
            sourcedir = self.sourceDir(i)
            if self.repositoryPathOptions(i) == 'norecursive':
                self.__checkout(url,sourcedir,False)
            else:
                self.__checkout(url,sourcedir,False)
            i += 1
        return True

    def __checkout( self, url, sourcedir, recursive=True ):
        """internal method for subversion checkout and update"""
        option = ""
        if recursive:
            option = "-N" 
            
        if os.path.exists( sourcedir ):
            cmd = "%s/svn update %s %s %s" % ( self.svnInstallDir, option, url, sourcedir )
        else:
            cmd = "%s/svn checkout %s %s %s" % (self.svnInstallDir, option, url, sourcedir )

        return self.system( cmd )
