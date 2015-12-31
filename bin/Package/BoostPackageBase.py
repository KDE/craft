# -*- coding: utf-8 -*-
# this package contains functions to check the current compiler
# copyright:
# Hannah von Reth <vonreth@kde.org>
import EmergeDebug
from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.BoostBuildSystem import *
from Packager.TypePackager import *

class BoostPackageBase (PackageBase, MultiSource, BoostBuildSystem, TypePackager):
    """provides a base class for cmake packages from any source"""
    def __init__(self):
        EmergeDebug.debug("BoostPackageBase.__init__ called", 2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        BoostBuildSystem.__init__(self)
        TypePackager.__init__(self)
