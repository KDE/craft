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

        self.__sourceClass = None
        if not self.subinfo.hasSvnTarget() and not self.subinfo.hasTarget():
            if "master" in self.subinfo.svnTargets:
                self.subinfo.svnTargets[self.buildTarget] = "{0}|{1}".format(self.subinfo.svnTargets["master"], self.buildTarget)

        if self.subinfo.hasSvnTarget():
            url = self.subinfo.svnTarget()
            sourceType = utils.getVCSType(url)
            if sourceType == "svn":
                self.__sourceClass = SvnSource
            elif sourceType == "git":
                self.__sourceClass = GitSource
        elif self.subinfo.hasTarget():
            self.__sourceClass = ArchiveSource

        if self.__sourceClass:
            self.__class__.__bases__ += (self.__sourceClass,)
            self.__sourceClass.__init__(self)

    # todo: find a more general way to publish all members
    def fetch(self):
        CraftCore.debug.trace("MultiSource fetch")
        return self.__sourceClass.fetch(self)

    def checkDigest(self, downloadRetries=3):
        CraftCore.debug.trace("MultiSource checkDigest")
        return self.__sourceClass.checkDigest(self, downloadRetries)

    def unpack(self):
        CraftCore.debug.trace("MultiSource unpack")
        return self.__sourceClass.unpack(self)

    def localFileNames(self):
        CraftCore.debug.trace("MultiSource localFileNames")
        return self.__sourceClass.localFileNames(self)

    def checkoutDir(self, index=0):
        CraftCore.debug.trace("MultiSource checkoutDir")
        return self.__sourceClass.checkoutDir(self, index=index)

    def sourceDir(self):
        CraftCore.debug.trace("MultiSource sourceDir")
        return self.__sourceClass.sourceDir(self)

    def repositoryUrl(self, index=0):
        CraftCore.debug.trace("MultiSource repositoryUrl")
        return self.__sourceClass.repositoryUrl(self, index)

    def repositoryUrlCount(self):
        CraftCore.debug.trace("MultiSource repositoryUrlCount")
        return self.__sourceClass.repositoryUrlCount(self)

    def applyPatches(self):
        CraftCore.debug.trace("MultiSource applyPatches")
        return self.__sourceClass.applyPatches(self)

    def createPatch(self):
        CraftCore.debug.trace("MultiSource createPatch")
        return self.__sourceClass.createPatch(self)

    def getUrls(self):
        CraftCore.debug.trace("MultiSource getUrls")
        return self.__sourceClass.getUrls(self)

    def sourceVersion(self):
        CraftCore.debug.trace("MultiSource sourceVersion")
        return self.__sourceClass.sourceVersion(self)

    def sourceRevision(self):
        CraftCore.debug.trace("MultiSource sourceVersion")
        return self.__sourceClass.sourceRevision(self)

    def printSourceVersion(self):
        CraftCore.debug.trace("MultiSource printSourceVersion")
        return self.__sourceClass.printSourceVersion(self)
