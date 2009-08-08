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
        
    def __getUrl( self, index ):
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

    def __splitUrl( self, url ):
        """ split url into real url and url option"""
        if url.find('#') <> -1:
            return url.split('#')
        return [url,""]
        
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

    def repositoryBasePath( self ):
        """ this function should return the base path to the KDE repository """
        if ( os.getenv("KDESVNSERVER") == None ):
            server = "svn://anonsvn.kde.org"
        else:
            server = os.getenv("KDESVNSERVER")
        
        return server + '/home/kde/'
        
    def repositoryPathCount( self ):
        if not self.subinfo.hasSvnTarget():
            return 0
        u = self.subinfo.svnTarget()
        if u.find(';') == -1:
            return 1
        urls = u.split(';')
        return len(urls)
    
    def repositoryPath( self, index=0 ):
        """this function return the full url into a version system based repository"""
        if self.subinfo.hasSvnTarget():
            u1 = self.__getUrl(index)
            (u,dummy) = self.__splitUrl(u1)
            # check relative kde url
            if u.find("://") == -1: 
                if ( os.getenv("KDESVNSERVER") == None ):
                    server = "svn://anonsvn.kde.org"
                else:
                    server = os.getenv("KDESVNSERVER")
            
                url = server + '/home/kde/' + u
            else:
                url = u
            return url            
        else:
            return False
            
    def repositoryPathOptions( self, index=0 ):
        """this function return optional options for the repository url at position 'index'"""
        if self.subinfo.hasSvnTarget():
            u = self.__getUrl(index)
            (dummy,option) = self.__splitUrl(u)
            return option
        return None

    def sourceDir(self, index=0 ): 
        if not self.noCopy:
            # need to check index ?
            sourcedir = self.workDir()
            return sourcedir
        else:
            if self.subinfo.hasSvnTarget():
                u = self.__getUrl(index)
                (url,dummy) = self.__splitUrl(u)

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

