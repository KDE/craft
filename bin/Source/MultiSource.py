#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from pathlib import Path

import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Source.ArchiveSource import ArchiveSource
from Source.DirSource import DirSource
from Source.GitSource import GitSource
from Source.SourceBase import SourceBase
from Source.SvnSource import SvnSource


class MultiSource(SourceBase):
    """provides multi source type api"""

    def __init__(self, package: CraftPackageObject):
        SourceBase.__init__(self, package)
        CraftCore.debug.trace("MultiSource __init__")
        self.__sourceClass = None

    @property
    def _sourceClass(self):
        # don't access those during the construction but only on demand
        if not self.__sourceClass:
            if self.subinfo.options.dynamic.srcDir or ("ContinuousIntegration", "SourceDir") in CraftCore.settings:
                self.__sourceClass = DirSource
            elif self.subinfo.hasSvnTarget():
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
                self.__sourceClass.__init__(self, self.package)
        return self.__sourceClass

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

    def sourceDir(self, dummyIndex=0) -> Path:
        CraftCore.debug.trace("MultiSource sourceDir")
        if hasattr(self._sourceClass, "sourceDir"):
            return self._sourceClass.sourceDir(self)
        return Path()

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
        if self.subinfo.revision:
            return self.subinfo.revision
        return self._sourceClass.sourceRevision(self)

    def printSourceVersion(self):
        CraftCore.debug.trace("MultiSource printSourceVersion")
        return self._sourceClass.printSourceVersion(self)
