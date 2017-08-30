#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from CraftBase import *


class SourceBase(CraftBase):
    """ implements basic stuff required for all sources"""

    def __init__(self):
        craftDebug.trace("SourceBase.__init__ called")
        CraftBase.__init__(self)

    def fetch(self, dummyRepoSource=None):
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

        if self.subinfo.targetSourceSuffix() != None:
            sourcedir = "%s-%s" % (sourcedir, self.subinfo.targetSourceSuffix())

        if self.subinfo.hasTargetSourcePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.targetSourcePath())
        craftDebug.log.debug("using sourcedir: " + sourcedir)
        return sourcedir

    def applyPatches(self):
        """apply patches if available"""
        craftDebug.trace("SourceBase.applyPatches called")
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            patches = self.subinfo.patchesToApply()
            if not isinstance(patches, list):
                patches = list([patches])
            # pylint: disable=W0142
            # do not warn about * magic
            return set(self.applyPatch(*x) for x in patches) == set([True])
        return True

    def applyPatch(self, fileName, patchdepth, srcdir=None):
        """base implementation for applying a single patch to the source"""
        craftDebug.trace("SourceBase.applyPatch called")
        if not fileName:
            return True
        if not srcdir:
            srcdir = self.sourceDir()
        patchfile = os.path.join(self.packageDir(), fileName)
        # TODO: integrate utils.applyPatch() here and remove it from utils().
        # and change packages in blueprints accordingly
        return utils.applyPatch(srcdir, patchfile, patchdepth)

    def createPatch(self):
        """create patch file from source into the related package dir. The patch file is named autocreated.patch"""
        utils.abstract()

    def getUrls(self):
        """return the urls that will be downloaded/checked out"""
        return True

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

    def sourceRevision(self):
        """
        :return: Same as sourceVersion for Cvs systems, None for all other
        """
        return None

    def printSourceVersion(self):
        """ return the current revision or version of the source directory,
            return True in case it is not applicable and give out nothing """
        print(self.sourceVersion())
        return True
