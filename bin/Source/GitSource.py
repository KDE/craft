# -*- coding: utf-8 -*-
# git support

from VersionSystemSourceBase import *
import os
import utils
import shells

class GitSource (VersionSystemSourceBase):
    """git support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)        
        self.shell = MSysShell()

    def unpack( self, repoUrl ):
        svndir = os.path.join( self.downloaddir, "svn-src" )
        
        ret = True
        if ( not self.noFetch ):
            safePath = os.environ["PATH"]
            os.environ["PATH"] = os.path.join(self.rootdir, "git", "bin") + ";" + safePath
            if os.path.exists( self.svndir ):
                """if directory already exists, simply do a pull but obey to offline"""
                ret = self.shell.execute( self.svndir, "git", "pull" )
            else:
                """it doesn't exist so clone the repo"""
                ret = self.shell.execute( svndir, "git", "clone %s %s" % ( repoUrl, self.package ) )
            os.environ["PATH"] = safePath
        else:
            utils.debug( "skipping git fetch (--offline)" )
        return ret
