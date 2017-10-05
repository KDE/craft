from BuildSystem.MSBuildBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import *
from Source.MultiSource import *


class MSBuildPackageBase(PackageBase, MultiSource, MSBuildBuildSystem, TypePackager):
    """provides a base class for MSBuild packages from any source"""

    def __init__(self):
        CraftCore.log.debug("MSBuildPackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        MSBuildBuildSystem.__init__(self)
        TypePackager.__init__(self)
