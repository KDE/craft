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
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            return super().fetch()
        return True


    def unpack(self):
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            return super().unpack()
        return True

    def sourceRevision(self):
        if self.subinfo.hasTarget() or self.subinfo.hasSvnTarget():
            return super().sourceRevision()
        return True

    # from PackagerBase
    def createPackage(self):
        return True

    def preArchive(self):
        return True
