from Package.SourceOnlyPackageBase import *
import portage


class VirtualPackageBase(SourceOnlyPackageBase):
    """provides a base class for virtual packages"""

    def __init__(self):
        craftDebug.log.debug("VirtualPackageBase.__init__ called")
        SourceOnlyPackageBase.__init__(self)

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

    def sourceVersion(self):
        return ""

    def sourceRevision(self):
        return ""
