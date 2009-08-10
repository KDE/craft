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
                self.__tryCheckoutFromRoot(url,sourcedir,False)
            else:
                self.__tryCheckoutFromRoot(url,sourcedir,True)
            i += 1
        return True

    def __splitPath(self, path):
        """ split a path into a base part and a relative repository url. 
        The delimiters are currently 'trunk', 'branches' and 'tags'. 
        """
        pos=path.find('trunk')
        if pos == -1:
            pos=path.find('branches')
            if pos == -1:
                pos=path.find('tags')
        if pos == -1:
            ret = [path,None]
        else:
            ret = [path[:pos-1], path[pos:]]
        return ret

    def __tryCheckoutFromRoot ( self, url, sourcedir, recursive=True ):
        """This method checkout source with svn informations from 
        the svn root repository directory. It detects the svn root 
        by searching the predefined root subdirectories 'trunk', 'branches' 
        and 'tags' which will probably fit for most servers
        """
        (urlBase,urlPath) = self.__splitPath(url)
        if urlPath == None:
            return self.__checkout(url, sourcedir, recursive)
        
        (srcBase,srcPath)  = self.__splitPath(sourcedir)
        if srcPath == None: 
            return self.__checkout(url, sourcedir, recursive)
        
        urlRepo = urlBase
        srcDir = srcBase
        urlParts = urlPath.split('/')
        pathSep = '/'
        srcParts = srcPath.split(pathSep)
        
        # url and source parts not match 
        if len(urlParts) <> len(srcParts):
            return self.__checkout(url, sourcedir, recursive)
        
        for i in range(0,len(urlParts)-1):
            urlPart = urlParts[i]
            srcPart = srcParts[i]
            if ( urlPart == "" ):
                continue
            
            urlRepo +=  '/' + urlPart
            srcDir +=  pathSep + srcPart
            
            if os.path.exists(srcDir): 
                continue
            self.__checkout( urlRepo, srcDir, False )
            
        self.__checkout( url, sourcedir, recursive )
    
    def __checkout( self, url, sourcedir, recursive=True ):
        """internal method for subversion checkout and update"""
        option = ""
        if not recursive:
            option = "--depth=files" 
            
        if utils.verbose() < 2: 
            option += " --quiet"
            
        if os.path.exists( sourcedir ):
            cmd = "%s/svn update %s %s %s" % ( self.svnInstallDir, option, url, sourcedir )
        else:
            cmd = "%s/svn checkout %s %s %s" % (self.svnInstallDir, option, url, sourcedir )

        return utils.system( cmd )
