#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.BinaryBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import *
from Source.MultiSource import *


class BinaryPackageBase(PackageBase, MultiSource, BinaryBuildSystem, TypePackager):
    """provides a base class for binary packages"""

    def __init__(self):
        CraftCore.log.debug("BinaryPackageBase.__init__ called")
        PackageBase.__init__(self)
        BinaryBuildSystem.__init__(self)
        MultiSource.__init__(self)
        TypePackager.__init__(self)
