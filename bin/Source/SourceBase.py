#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from EmergeBase import *

class SourceBase(EmergeBase):
    """ implements basic stuff required for all sources"""
    def __init__(self, className=None):
        utils.trace( "SourceBase.__init__ called", 2 )
        EmergeBase.__init__(self, className)
        self.url = ""

    def setProxy(self):
        """set proxy for fetching sources - the default implementation is to set the
        environment variables http_proxy and ftp_proxy"""
        (host, port, username, password) = self.proxySettings()
        if host == None:
            return

        name = ""
        if username != None and password != None:
            name = "%s:%s@" % (username, password)

        proxy = "http://%s%s:%s" % (name, host, port)
        utils.putenv("http_proxy", proxy)
        utils.putenv("ftp_proxy", proxy)

    def fetch(self):
        """fetch the source from a remote host and save it into a local destination"""
        utils.abstract()

    def checkDigest(self):
        """check source digest of the package."""
        return True

    def unpack(self):
        """unpack the source into a local destination."""
        utils.abstract()

    def sourceDir(self, dummyIndex=0):
        """ return absolute path of the directory where sources are fetched into.
        utils.trace( "SourceBase.sourceDir called", 0 )
        The subinfo class members @ref targetSrcSuffic and @ref targetInstSrc
        controls parts of the name of the generated path. """

        if self.subinfo.options.unpack.unpackIntoBuildDir:
            sourcedir = self.buildDir()
        else:
            sourcedir = self.workDir()
        if self.buildSystemType == 'binary':
            sourcedir = self.imageDir()

        if self.subinfo.targetSourceSuffix() != None:
            sourcedir = "%s-%s" % (sourcedir, self.subinfo.targetSourceSuffix())

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())
        utils.debug( "using sourcedir: " + sourcedir, 1 )
        return sourcedir

    def applyPatches(self):
        """apply patches if available"""
        utils.trace( "SourceBase.applyPatches called", 0 )
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            patches = self.subinfo.patchesToApply()
            if type(patches) == list:
                ret = True
                for fileName, patchdepth in patches:
                    utils.debug( "applying %s with patchlevel: %s" % ( fileName, patchdepth ) )
                    if not self.applyPatch( fileName, patchdepth ):
                        utils.warning( "applying %s failed!" % ( fileName ) )
                        ret = False
                return ret
            else:
                ( fileName, patchdepth ) = patches
                return self.applyPatch( fileName, patchdepth )

        return True

    def applyPatch(self, fileName, patchdepth, srcdir=None ):
        """base implementation for applying a single patch to the source"""
        utils.trace( "SourceBase.applyPatch called", 2 )
        if not srcdir:
            srcdir = self.sourceDir()
        if fileName:
            patchfile = os.path.join ( self.packageDir(), fileName )
            return utils.applyPatch( srcdir, patchfile, patchdepth )
        return True

    def createPatch(self):
        """create patch file from source into the related package dir. The patch file is named autocreated.patch"""
        utils.abstract()

    def repositoryUrl(self, dummyIndex=0):
        """use this to get one of multiple repository paths; these can be download urls as well"""
        utils.abstract()

    def repositoryUrlCount(self):
        """use this to get number of repository paths"""
        utils.abstract()

    def localFileNamesBase(self):
        utils.abstract()

    def sourceVersion(self):
        """ return the current revision or version of the source directory,
            return True in case it is not applicable and give out nothing """
        return True
