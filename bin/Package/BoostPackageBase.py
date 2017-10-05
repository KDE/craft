# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Hannah von Reth <vonreth@kde.org>
from BuildSystem.BoostBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import *
from Source.MultiSource import *


class BoostPackageBase(PackageBase, MultiSource, BoostBuildSystem, TypePackager):
    """provides a base class for cmake packages from any source"""

    def __init__(self):
        CraftCore.log.debug("BoostPackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        BoostBuildSystem.__init__(self)
        TypePackager.__init__(self)
