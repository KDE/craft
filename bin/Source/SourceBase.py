# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from EmergeBase import *

class SourceBase(EmergeBase):
    """ implements basic stuff required for all sources"""
    def __init__(self):
        utils.debug( "SourceBase.__init__ called", 2 )
        EmergeBase.__init__(self)
        self.url = ""
        
    def setProxy(self):
        """set proxy for fetching sources - the default implementation is to set the 
        environment variables http_proxy and ftp_proxy"""
        (host, port, username, password) = self.proxySettings()
        if host == None:
            return 

        name = ""
        if username != None and password != None:
            name = "%s:%s@" % (username,password)
        
        proxy = "http://%s%s:%s" % (name,host,port)
        utils.putenv("http_proxy", proxy)
        utils.putenv("ftp_proxy", proxy)
       
    def fetch(self): 
        """fetch the source from a remote host and save it into a local destination"""
        abstract()

    def unpack(self): 
        """unpack the source into a local destination."""
        abstract()

    def sourceDir(self, index=0):
        sourcedir = self.workDir()
        if hasattr(self, 'buildSystemType') and self.buildSystemType == 'binary':
            sourcedir = self.imageDir()

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())
        utils.debug( "using sourcedir: " + sourcedir, 1 )
        return sourcedir

    def applyPatches(self):
        """apply patches is available"""
        utils.debug( "SourceBase.applyPatches called", 2 )

        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            ( file, patchdepth ) = self.subinfo.patchesToApply()
            if file:
                patchfile = os.path.join ( self.packageDir(), file )
                srcdir = os.path.join ( self.sourceDir() )
                return utils.applyPatch( srcdir, patchfile, patchdepth )
        return True

    def createPatch(self):
        """create patch file from source into the related package dir. The patch file is named autocreated.patch"""
        abstract()

    def repositoryUrl(self,index=0):
        """use this to get one of multiple repository paths; these can be download urls as well"""
        abstract()

    def repositoryUrlCount(self):
        """use this to get number of repository paths"""
        abstract()

    def localFileNamesBase(self):
        abstract()

    def sourceVersion(self):
        """ return the current revision or version of the source directory, 
            return True in case it is not applicable and give out nothing """
        return True
