from BuildSystem.PipBuildSystem import PipBuildSystem
from Package.PackageBase import PackageBase
from Packager.PackagerBase import PackagerBase
from Source.MultiSource import MultiSource
from CraftCore import CraftCore


class PipPackageBase(PackageBase, MultiSource, PipBuildSystem, PackagerBase):
    """provides a base class for pip packages"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("PipPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        PipBuildSystem.__init__(self, **kwargs)
        PackagerBase.__init__(self, **kwargs)

    def fetch(self):
        if self._sourceClass:
            return self._sourceClass.fetch(self)
        return True

    def unpack(self):
        if self._sourceClass:
            return self._sourceClass.unpack(self)
        return True

    def sourceRevision(self):
        if self._sourceClass:
            return self._sourceClass.sourceRevision(self)
        return ""

    # from PackagerBase
    def createPackage(self):
        return True

    def preArchive(self):
        return True
