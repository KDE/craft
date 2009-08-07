
from PackageBase import *;
from Source.SvnSource import *;
from BuildSystem.CMakeBuildSystem import *;
from Packager.KDEWinPackager import *;

## \todo rename to CMakePackage
class CMakePackageBase (PackageBase, SvnSource, CMakeBuildSystem, KDEWinPackager):
    """provides a base class for cmake packages from any source"""
    def __init__(self):
        utils.debug("CMakePackageBase.__init__ called",2)
        PackageBase.__init__(self)
        SvnSource.__init__(self)
        CMakeBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
