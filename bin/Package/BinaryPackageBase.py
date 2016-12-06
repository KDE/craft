#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import CraftDebug
from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.BinaryBuildSystem import *
from Packager.TypePackager import *

class BinaryPackageBase (PackageBase, MultiSource, BinaryBuildSystem, TypePackager):
    """provides a base class for binary packages"""
    def __init__(self):
        CraftDebug.debug("BinaryPackageBase.__init__ called", 2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        TypePackager.__init__(self)
