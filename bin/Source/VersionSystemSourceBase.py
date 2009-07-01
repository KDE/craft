# -*- coding: utf-8 -*-

from SourceBase import *
import os

class VersionSystemSourceBase (SourceBase):
    """abstract base class for version system support"""

    noFetch = False

    # host part of svn server 
    kdesvnserver = ""

    # local checkout root path
    kdesvndir = ""
        
    # complete local path for currently used source
    svndir = ""
        
    def __init__(self):
        SourceBase.__init__(self)
        
    def unpack(self):
        self.applyPatches()

        if not self.noClean:
            if utils.verbose > 0:
                print "cleaning %s" % self.builddir
            self.enterBuildDir()
            utils.cleanDirectory( self.builddir )
        
        if not self.noCopy:
            if utils.verbose > 0:
                print "copying %s to %s" % (self.sourcedir, self.builddir)
            self.enterBuildDir()
            utils.copySrcDirToDestDir(self.sourcedir, self.builddir)
        return True;

    def repositoryPath( self ):
        """this function should return the full path into the repository"""
        if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
            return self.subinfo.svnTargets[ self.subinfo.buildTarget ]
        else:
            return False
