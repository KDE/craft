from BuildSystem.PipBuildSystem import *
from Package.PackageBase import *
from Packager.PackagerBase import *
from Source.SourceBase import *


class PipPackageBase(PackageBase, SourceBase, PipBuildSystem, PackagerBase):
    """provides a base class for pip packages"""

    def __init__(self):
        CraftCore.log.debug("PipPackageBase.__init__ called")
        PackageBase.__init__(self)
        SourceBase.__init__(self)
        PipBuildSystem.__init__(self)
        PackagerBase.__init__(self)

    # from SourceBase:
    def fetch(self):
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
