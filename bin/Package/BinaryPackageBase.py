
from PackageBase import *;
from Source.ArchiveSource import *;
from BuildSystem.BinaryBuildSystem import *;

class BinaryPackageBase (PackageBase, ArchiveSource, BinaryBuildSystem):
    """provides a base class for binary packages"""
    def __init__(self):
        utils.debug("BinaryPackageBase.__init__ called",2)
        PackageBase.__init__(self)
        ArchiveSource.__init__(self)
        BinaryBuildSystem.__init__(self)
