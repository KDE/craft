# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Patrick von Reth <patrick.vonreth [AT] gmail [DOT] com>


from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.BoostBuildSystem import *
from Packager.KDEWinPackager import *

class BoostPackageBase (PackageBase, MultiSource, BoostBuildSystem, KDEWinPackager):
    """provides a base class for cmake packages from any source"""
    def __init__(self):
        utils.debug("BoostPackageBase.__init__ called", 2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        BoostBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
