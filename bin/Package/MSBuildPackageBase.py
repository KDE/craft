from BuildSystem.MSBuildBuildSystem import MSBuildBuildSystem
from CraftCore import CraftCore
from Package.PackageBase import PackageBase
from Packager.TypePackager import TypePackager
from Source.MultiSource import MultiSource


class MSBuildPackageBase(PackageBase, MultiSource, MSBuildBuildSystem, TypePackager):
    """provides a base class for MSBuild packages from any source"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("MSBuildPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        MSBuildBuildSystem.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)
