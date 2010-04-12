# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

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
        
    def getUrl( self, index ):
        """get the url at position 'index' from a ';' separated list of urls"""
        u = self.subinfo.svnTarget()
        if u.find(';') == -1:
            if index == 0:
                return u
            else:
                return None
        # urls are a list
        urls = u.split(';')
        if index >= len(urls):
            return None
        
        u = urls[index]
        return u

    def splitUrl( self, url ):
        """ split url into real url and url option. the delimiter is '#'"""
        if url.find('#') <> -1:
            return url.split('#')
        return [url,""]
        
    def __repositoryBaseUrl( self ):
        """ this function return the base url to the KDE repository """
        if ( os.getenv("KDESVNSERVER") == None ):
            server = "svn://anonsvn.kde.org"
        else:
            server = os.getenv("KDESVNSERVER")
        
        return server + '/home/kde/'

    def unpack(self):
        self.applyPatches()
        self.enterBuildDir()

        if not self.noClean:
            if utils.verbose > 0:
                print "cleaning %s" % self.buildDir()
            utils.cleanDirectory( self.buildDir() )
        
        if not self.noCopy:
            if utils.verbose > 0:
                print "copying %s to %s" % (self.sourceDir(), self.buildDir())
            utils.copySrcDirToDestDir(self.sourceDir(), self.buildDir())
        return True;
        
    def repositoryUrlCount( self ):
        """return the number of provided repository url's. Multiple repository urls' are delimited by ';'"""
        if not self.subinfo.hasSvnTarget():
            return 0
        u = self.subinfo.svnTarget()
        if u.find(';') == -1:
            return 1
        urls = u.split(';')
        return len(urls)
    
    def repositoryUrl( self, index=0 ):
        """this function returns the full url into a version system based repository at position 'index'.
        See @ref repositoryUrlCount how to define multiple repository urls."""
        if self.subinfo.hasSvnTarget():
            u1 = self.getUrl(index)
            (u,dummy) = self.splitUrl(u1)
            # check relative kde url
            if u.find("://") == -1: 
                url= self.__repositoryBaseUrl() + u
            else:
                url = u
            return url            
        else:
            return False

    def repositoryUrlOptions( self, index=0 ):
        """this function return options for the repository url at position 'index'. 
        Options for a repository url are defined by adding '#' followed by the specific option. 
        """
        if self.subinfo.hasSvnTarget():
            u = self.getUrl(index)
            (dummy,option) = self.splitUrl(u)
            return option
        return None

    def sourceDir(self, index=0 ): 
        if not self.noCopy:
            # need to check index ?
            sourcedir = self.workDir()
            return sourcedir
        else:
            if self.subinfo.hasSvnTarget():
                u = self.getUrl(index)
                (url,dummy) = self.splitUrl(u)

                if url.find("://") == -1: 
                    if os.getenv("KDESVNDIR") == None:
                        sourcedir = os.path.join( self.downloadDir(), "svn-src", "kde", url )
                    else:
                        sourcedir = os.path.join( os.getenv("KDESVNDIR"), url )
                else:
                    sourcedir = os.path.join( self.downloadDir(), "svn-src", self.package )
            else:
                utils.die("svnTarget property not set for this target")
        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())

        utils.debug("using sourcedir: %s" % sourcedir,2)
        return sourcedir

