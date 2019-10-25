#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Source.ArchiveSource import ArchiveSource
from Source.GitSource import GitSource

from Source.SourceBase import *
from Source.SvnSource import SvnSource


class MultiSource(SourceBase):
    """ provides multi source type api """

    def __init__(self):
        SourceBase.__init__(self)
        CraftCore.debug.trace("MultiSource __init__")

        self._sourceClass = None
        if self.subinfo.hasSvnTarget():
            url = self.subinfo.svnTarget()
            sourceType = utils.getVCSType(url)
            if sourceType == "svn":
                self._sourceClass = SvnSource
            elif sourceType == "git":
                self._sourceClass = GitSource
        elif self.subinfo.hasTarget():
            self._sourceClass = ArchiveSource

        if self._sourceClass:
            self.__class__.__bases__ += (self._sourceClass,)
            self._sourceClass.__init__(self)

    # todo: find a more general way to publish all members
    def fetch(self):
        CraftCore.debug.trace("MultiSource fetch")
        return self._sourceClass.fetch(self)

    def checkDigest(self, downloadRetries=3):
        CraftCore.debug.trace("MultiSource checkDigest")
        return self._sourceClass.checkDigest(self, downloadRetries)

    def unpack(self):
        CraftCore.debug.trace("MultiSource unpack")
        return self._sourceClass.unpack(self)

    def localFileNames(self):
        CraftCore.debug.trace("MultiSource localFileNames")
        return self._sourceClass.localFileNames(self)

    def checkoutDir(self, index=0):
        CraftCore.debug.trace("MultiSource checkoutDir")
        return self._sourceClass.checkoutDir(self, index=index)

    def sourceDir(self):
        CraftCore.debug.trace("MultiSource sourceDir")
        return self._sourceClass.sourceDir(self)

    def repositoryUrl(self, index=0):
        CraftCore.debug.trace("MultiSource repositoryUrl")
        return self._sourceClass.repositoryUrl(self, index)

    def repositoryUrlCount(self):
        CraftCore.debug.trace("MultiSource repositoryUrlCount")
        return self._sourceClass.repositoryUrlCount(self)

    def applyPatches(self):
        CraftCore.debug.trace("MultiSource applyPatches")
        return self._sourceClass.applyPatches(self)

    def createPatch(self):
        CraftCore.debug.trace("MultiSource createPatch")
        return self._sourceClass.createPatch(self)

    def getUrls(self):
        CraftCore.debug.trace("MultiSource getUrls")
        return self._sourceClass.getUrls(self)

    def sourceVersion(self):
        CraftCore.debug.trace("MultiSource sourceVersion")
        return self._sourceClass.sourceVersion(self)

    def sourceRevision(self):
        CraftCore.debug.trace("MultiSource sourceVersion")
        return self._sourceClass.sourceRevision(self)

    def printSourceVersion(self):
        CraftCore.debug.trace("MultiSource printSourceVersion")
        return self._sourceClass.printSourceVersion(self)
