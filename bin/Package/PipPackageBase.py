from BuildSystem.PipBuildSystem import *
from Package.PackageBase import *
from Packager.PackagerBase import *
from Package.VirtualPackageBase import *
from Source.MultiSource import *

class PipPackageBase(PackageBase, PipBuildSystem, PackagerBase):
    """provides a base class for pip packages"""

    def __init__(self):
        CraftCore.log.debug("PipPackageBase.__init__ called")
        PackageBase.__init__(self)
        if self.subinfo.svnTarget():
            self.__class__.__bases__ += (MultiSource,)
            MultiSource.__init__(self)
        else:
            self.__class__.__bases__ += (VirtualPackageBase,)
            VirtualPackageBase.__init__(self)
        PipBuildSystem.__init__(self)
        PackagerBase.__init__(self)


    # from PackagerBase
    def createPackage(self):
        return True

    def preArchive(self):
        return True
