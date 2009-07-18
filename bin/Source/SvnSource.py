# -*- coding: utf-8 -*-
# subversion support
# todo needs dev-utils/subversion package, add some kind of tool requirement tracking for SourceBase derived classes 

from VersionSystemSourceBase import *
import os
import utils

class SvnSource (VersionSystemSourceBase):
    """subversion support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)
        
    def fetch( self, repopath=None, packagedir=None ):
        if repopath == None:
            repopath = self.repositoryPath()

        if packagedir == None:
            packagedir = self.packagedir
            
        ret = True
        if ( not self.noFetch ):
            if os.path.exists( self.sourceDir() ):
                cmd = "svn update %s %s" % ( repopath, self.sourceDir() )
            else:
                cmd = "svn checkout %s %s" % ( repopath, self.sourceDir() )
            utils.system( cmd ) or utils.die( "while perfoming svn command: %s" % cmd )
        else:
            utils.debug( "skipping svn fetch (--offline)" )
        return ret
