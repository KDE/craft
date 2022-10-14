#
# copyright (c) 2012 Hannah von Reth <vonreth@kde.org>
#
from BuildSystem.Qt5CoreBuildSystem import *
from Package.MaybeVirtualPackageBase import *
from Packager.TypePackager import *


class Qt5CorePackageBase(PackageBase, MultiSource, Qt5CoreBuildSystem, TypePackager):
    """provides a base class for qt5 modules"""

    def __init__(self):
        CraftCore.log.debug("Qt5CorePackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        Qt5CoreBuildSystem.__init__(self)
        TypePackager.__init__(self)
