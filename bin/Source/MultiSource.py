#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Source.ArchiveSource import ArchiveSource
from Source.GitSource import GitSource
from Source.HgSource import HgSource

from Source.SourceBase import *
from Source.SvnSource import SvnSource


class MultiSource(SourceBase):
    """ provides multi source type api """

    def __init__(self):
        SourceBase.__init__(self)
        CraftCore.debug.trace("MultiSource __init__")

        self.source = None
        if self.subinfo.hasSvnTarget():
            url = self.subinfo.svnTarget()
            sourceType = utils.getVCSType(url)
            if sourceType == "svn":
                self.source = SvnSource
            elif sourceType == "hg":
                self.source = HgSource
            elif sourceType == "git":
                self.source = GitSource
        elif self.subinfo.hasTarget():
            self.source = ArchiveSource

        if self.source:
            self.__class__.__bases__ += (self.source,)
            self.source.__init__(self)

    # todo: find a more general way to publish all members
    def fetch(self):
        CraftCore.debug.trace("MultiSource fetch")
        return self.source.fetch(self)

    def checkDigest(self):
        CraftCore.debug.trace("MultiSource checkDigest")
        return self.source.checkDigest(self)

    def unpack(self):
        CraftCore.debug.trace("MultiSource unpack")
        return self.source.unpack(self)

    def localFileNames(self):
        CraftCore.debug.trace("MultiSource localFileNames")
        return self.source.localFileNames(self)

    def checkoutDir(self, index=0):
        CraftCore.debug.trace("MultiSource checkoutDir")
        return self.source.checkoutDir(self, index=index)

    def sourceDir(self):
        CraftCore.debug.trace("MultiSource sourceDir")
        return CraftShortPath(self.source.sourceDir(self)).path(self.subinfo.options.needsShortPath)

    def repositoryUrl(self, index=0):
        CraftCore.debug.trace("MultiSource repositoryUrl")
        return self.source.repositoryUrl(self, index)

    def repositoryUrlCount(self):
        CraftCore.debug.trace("MultiSource repositoryUrlCount")
        return self.source.repositoryUrlCount(self)

    def applyPatches(self):
        CraftCore.debug.trace("MultiSource applyPatches")
        return self.source.applyPatches(self)

    def createPatch(self):
        CraftCore.debug.trace("MultiSource createPatch")
        return self.source.createPatch(self)

    def getUrls(self):
        CraftCore.debug.trace("MultiSource getUrls")
        return self.source.getUrls(self)

    def sourceVersion(self):
        CraftCore.debug.trace("MultiSource sourceVersion")
        return self.source.sourceVersion(self)

    def sourceRevision(self):
        CraftCore.debug.trace("MultiSource sourceVersion")
        return self.source.sourceRevision(self)

    def printSourceVersion(self):
        CraftCore.debug.trace("MultiSource printSourceVersion")
        return self.source.printSourceVersion(self)
