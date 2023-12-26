#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.QMakeBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import TypePackager
from Source.MultiSource import *


class QMakePackageBase(PackageBase, MultiSource, QMakeBuildSystem, TypePackager):
    """provides a base class for qmake packages from any source"""

    def __init__(self):
        CraftCore.log.debug("QMakePackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        QMakeBuildSystem.__init__(self)
        TypePackager.__init__(self)
