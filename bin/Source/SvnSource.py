# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# subversion support
## \todo needs dev-utils/subversion package, add some kind of tool requirement tracking for SourceBase derived classes 

from VersionSystemSourceBase import *

import os.path

import utils

class SvnSource (VersionSystemSourceBase):
    """subversion support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)
        self.options = None
        ## \todo add internal dependency for subversion package
        self.svnInstallDir = os.path.join(self.rootdir,'dev-utils','svn','bin')
        if not os.path.exists(self.svnInstallDir):
            utils.die("required subversion package not installed in %s" % self.svnInstallDir)
            
    def applyPatch(self, file, patchdepth):
        """apply a patch to a svn repository checkout"""
        if file:
            patchfile = os.path.join (self.packageDir(), file)
            # @todo check if this could be merged into SourceBase.applyPatch
            if self.noCopy:
                srcdir = self.sourceDir()
            else:
                srcdir = self.buildDir()
            return utils.applyPatch(srcdir, patchfile, patchdepth)
        return True

    def setProxy(self):
        """set proxy for fetching sources from subversion repository"""
        (host, port, username, password) = self.proxySettings()
        if host == None:
            return 

        proxyOptions = " --config-option servers:global:http-proxy-host=%s" % host
        proxyOptions += " --config-option servers:global:http-proxy-port=%s" % port
        if username != None:
            proxyOptions += " --config-option servers:global:http-proxy-username=%s" % username
            proxyOptions += " --config-option servers:global:http-proxy-password=%s" % password
        
        self.options = proxyOptions
            
    def fetch( self ):
        """ checkout or update an existing repository path """
        if self.noFetch:
            utils.debug( "skipping svn fetch (--offline)" )
            return True

        for i in range(0, self.repositoryUrlCount()):
            url = self.repositoryUrl(i)
            sourcedir = self.checkoutDir(i)
            if self.repositoryUrlOptions(i) == 'norecursive':
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
          
        self.setProxy()
        
        if self.options != None:
            option += self.options
            
        if self.subinfo.options.fetch.ignoreExternals:
            option += " --ignore-externals "

        url = utils.replaceVCSUrl( url )

        if os.path.exists( sourcedir ):
            cmd = "%s/svn update %s %s %s" % ( self.svnInstallDir, option, url, sourcedir )
        else:
            cmd = "%s/svn checkout %s %s %s" % (self.svnInstallDir, option, url, sourcedir )

        with utils.LockFile(utils.svnLockFileName()):
            return utils.system( cmd )

    def createPatch( self ):
        """create patch file from svn source into the related package dir. The patch file is named autocreated.patch"""
        cmd = "%s/svn diff %s > %s" % ( self.svnInstallDir, self.checkoutDir(), os.path.join( self.packageDir(), "%s-%s.patch" % ( self.package, str( datetime.date.today() ).replace('-', '') ) ) )
        with utils.LockFile(utils.svnLockFileName()):
            return utils.system( cmd )

    def sourceVersion( self ):
        """ return the revision returned by svn info """
        # first, change the output to always be english
        if "LANG" in os.environ:
            oldLanguage = os.environ["LANG"]
        else:
            oldLanguage = ""
        os.environ["LANG"] = "C"
        
        # set up the command
        cmd = "%s/svn info %s" % ( self.svnInstallDir, self.checkoutDir() )

        # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python
        tempfile = open( os.path.join( self.checkoutDir().replace('/', '\\'), ".emergesvninfo.tmp" ), "wb+" )
        
        # run the command
        with utils.LockFile(utils.svnLockFileName()):
            utils.system( cmd, outstream=tempfile )

        tempfile.seek(os.SEEK_SET)
        # read the temporary file and find the line with the revision
        for line in tempfile:
            if line.startswith("Revision: "):
                revision = line.replace("Revision: ", "").strip()
                break
        tempfile.close()
        
        # print the revision - everything else should be quiet now
        print revision
        os.environ["LANG"] = oldLanguage
        os.remove( os.path.join( self.checkoutDir().replace('/', '\\'), ".emergesvninfo.tmp" ) )
        return True