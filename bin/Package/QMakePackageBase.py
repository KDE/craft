
from PackageBase import *;
from Source.MultiSource import *;
from BuildSystem.QMakeBuildSystem import *;
from Packager.KDEWinPackager import *;

## \todo rename to QMakePackage
class QMakePackageBase (PackageBase, MultiSource, QMakeBuildSystem, KDEWinPackager):
    """provides a base class for qmake packages from any source"""
    def __init__(self):
        utils.debug("QMakePackageBase.__init__ called",2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        QMakeBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
