#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.MakeFileBuildSystem import MakeFileBuildSystem
from CraftCore import CraftCore
from Package.PackageBase import PackageBase
from Packager.TypePackager import TypePackager
from Source.MultiSource import MultiSource


class MakeFilePackageBase(PackageBase, MultiSource, MakeFileBuildSystem, TypePackager):
    """provides a base class for simple makefile based packages from any source"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("MakeFilePackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        MakeFileBuildSystem.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)
