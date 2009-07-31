# -*- coding: utf-8 -*-
# subversion support
## \todo needs dev-utils/subversion package, add some kind of tool requirement tracking for SourceBase derived classes 

from VersionSystemSourceBase import *
import os
import utils

class SvnSource (VersionSystemSourceBase):
    """subversion support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)
        self.svnInstallDir = os.path.join(self.rootdir,'dev-utils','svn','bin')
        if not os.path.exists(self.svnInstallDir):
            die("required subversion package not installed")
        
    def fetch( self, repopath=None, packagedir=None ):
        if repopath == None:
            repopath = self.repositoryPath()

        if packagedir == None:
            packagedir = self.packageDir()
            
        ret = True
        if ( not self.noFetch ):
        
            if os.path.exists( self.sourceDir() ):
                cmd = "%s/svn update %s %s" % ( self.svnInstallDir, repopath, self.sourceDir() )
            else:
                cmd = "%s/svn checkout %s %s" % (self.svnInstallDir, repopath, self.sourceDir() )
            utils.system( cmd ) or utils.die( "while perfoming svn command: %s" % cmd )
        else:
            utils.debug( "skipping svn fetch (--offline)" )
        return ret
