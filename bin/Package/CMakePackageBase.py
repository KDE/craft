#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.CMakeBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import TypePackager
from Source.MultiSource import *


class CMakePackageBase(PackageBase, MultiSource, CMakeBuildSystem, TypePackager):
    """provides a base class for cmake packages from any source"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("CMakePackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        CMakeBuildSystem.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)
