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
                print "cleaning %s" % self.buildDir()
            self.enterBuildDir()
            utils.cleanDirectory( self.buildDir() )
        
        if not self.noCopy:
            if utils.verbose > 0:
                print "copying %s to %s" % (self.sourceDir(), self.buildDir())
            self.enterBuildDir()
            utils.copySrcDirToDestDir(self.sourceDir(), self.buildDir())
        return True;

    def repositoryPath( self ):
        """this function should return the full path into the repository"""
        if self.subinfo.hasSvnTarget():
            url = self.subinfo.svnTarget()
            if url.find("://") == -1: 
                return os.environ["KDESVNSERVER"] + '/home/kde/' + url
            else:
                return url
        else:
            return False
            
    def sourceDir(self): 
        if not self.noCopy:
            sourcedir = self.workDir()
        else:
            if self.subinfo.hasSvnTarget():
                url = self.subinfo.svnTarget()
                if url.find("://") == -1: 
                    sourcedir = os.path.join( os.environ["KDESVNDIR"], url )
                else:
                    sourcedir = os.path.join( self.downloadDir(), "svn-src", self.package )
            else:
                utils.die("svnTarget property not set for this target")
        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())

        utils.debug("using sourcedir: %s" % sourcedir,2)
        return sourcedir

