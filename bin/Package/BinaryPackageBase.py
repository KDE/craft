# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from PackageBase import *;
from Source.ArchiveSource import *;
from BuildSystem.BinaryBuildSystem import *;
from Packager.KDEWinPackager import *;

## \todo rename to BinaryPackage
class BinaryPackageBase (PackageBase, ArchiveSource, BinaryBuildSystem, KDEWinPackager):
    """provides a base class for binary packages"""
    def __init__(self):
        utils.debug("BinaryPackageBase.__init__ called",2)
        PackageBase.__init__(self)
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
