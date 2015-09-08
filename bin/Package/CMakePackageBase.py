#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.CMakeBuildSystem import *
from Packager.SevenZipPackager import *

class CMakePackageBase (PackageBase, MultiSource, CMakeBuildSystem, SevenZipPackager):
    """provides a base class for cmake packages from any source"""
    def __init__(self):
        utils.debug("CMakePackageBase.__init__ called", 2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        CMakeBuildSystem.__init__(self)
        SevenZipPackager.__init__(self)
