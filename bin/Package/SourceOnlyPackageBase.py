from BuildSystem import BuildSystemBase
from BuildSystem.BuildSystemBase import *
from Package.PackageBase import *
from Packager.PackagerBase import *
from Source.MultiSource import *


class SourceOnlyPackageBase(PackageBase, MultiSource, BuildSystemBase, PackagerBase):
    """provides a base class for source dependency packages"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("SourceOnlyPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        BuildSystemBase.__init__(self, **kwargs, typeName="")
        PackagerBase.__init__(self, **kwargs)

    # from BuildSystemBase:
    def configure(self):
        return True

    def install(self):
        return True

    def uninstall(self):
        return True

    def make(self):
        return True

    # from PackagerBase:
    def createPackage(self):
        return True
