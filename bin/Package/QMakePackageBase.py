#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.QMakeBuildSystem import *
from Packager.SevenZipPackager import *

class QMakePackageBase (PackageBase, MultiSource, QMakeBuildSystem, SevenZipPackager):
    """provides a base class for qmake packages from any source"""
    def __init__(self):
        utils.debug("QMakePackageBase.__init__ called", 2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        QMakeBuildSystem.__init__(self)
        SevenZipPackager.__init__(self)
