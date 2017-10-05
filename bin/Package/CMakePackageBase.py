#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.CMakeBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import *
from Source.MultiSource import *


class CMakePackageBase(PackageBase, MultiSource, CMakeBuildSystem, TypePackager):
    """provides a base class for cmake packages from any source"""

    def __init__(self):
        CraftCore.log.debug("CMakePackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        CMakeBuildSystem.__init__(self)
        TypePackager.__init__(self)
