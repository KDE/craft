from CraftCore import CraftCore
from Package.SourceOnlyPackageBase import SourceOnlyPackageBase
from Source.MultiSource import MultiSource


# a special package providing source components for another module.
# see clang
class SourceComponentPackageBase(SourceOnlyPackageBase):
    def __init__(self, **kwargs):
        CraftCore.log.debug("SourceComponentPackageBase.__init__ called")
        SourceOnlyPackageBase.__init__(self, **kwargs)
        self.subinfo.options.package.disableBinaryCache = True

    def fetch(self, noop=True):
        if noop:
            return True
        return MultiSource.fetch(self)

    def unpack(self, noop=True):
        if noop:
            return True
        return MultiSource.unpack(self)


class VirtualPackageBase(SourceComponentPackageBase):
    """provides a base class for virtual packages"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("VirtualPackageBase.__init__ called")
        SourceComponentPackageBase.__init__(self, **kwargs)
        self.subinfo.shelveAble = False

    def createPatch(self):
        return True

    def getUrls(self):
        return True

    def repositoryUrl(self, dummyIndex=0):
        return ""

    def repositoryUrlCount(self):
        return 0

    def sourceVersion(self):
        return ""

    def sourceRevision(self):
        return ""
