from BuildSystem.PipBuildSystem import *
from Package.PackageBase import *
from Packager.PackagerBase import *
from Package.VirtualPackageBase import *
from Source.MultiSource import *

class PipPackageBase(PackageBase, MultiSource, PipBuildSystem, PackagerBase):
    """provides a base class for pip packages"""

    def __init__(self):
        CraftCore.log.debug("PipPackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        PipBuildSystem.__init__(self)
        PackagerBase.__init__(self)

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
