# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Hannah von Reth <vonreth@kde.org>
from BuildSystem.BoostBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import TypePackager
from Source.MultiSource import *


class BoostPackageBase(PackageBase, MultiSource, BoostBuildSystem, TypePackager):
    """provides a base class for cmake packages from any source"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("BoostPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        BoostBuildSystem.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)
