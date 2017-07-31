from CraftDebug import craftDebug
from Package.PackageBase import *
from Source.SourceBase import *
from BuildSystem.PipBuildSystem import *
from Packager.PackagerBase import *


class PipPackageBase(PackageBase, SourceBase, PipBuildSystem, PackagerBase):
    """provides a base class for pip packages"""

    def __init__(self):
        craftDebug.log.debug("PipPackageBase.__init__ called")
        PackageBase.__init__(self)
        SourceBase.__init__(self)
        PipBuildSystem.__init__(self)
        PackagerBase.__init__(self)

    # from SourceBase:
    def fetch(self, dummyRepoSource=None):
        return True

    def unpack(self):
        return True

    def createPatch(self):
        return True

    def getUrls(self):
        return True

    def repositoryUrl(self, dummyIndex=0):
        return ""

    def repositoryUrlCount(self):
        return 0

    def localFileNamesBase(self):
        return []

    # from PackagerBase
    def createPackage(self):
        return True

    def preArchive(self):
        return True
