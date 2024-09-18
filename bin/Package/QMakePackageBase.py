#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.QMakeBuildSystem import QMakeBuildSystem
from CraftCore import CraftCore
from Package.PackageBase import PackageBase
from Packager.TypePackager import TypePackager
from Source.MultiSource import MultiSource


class QMakePackageBase(PackageBase, MultiSource, QMakeBuildSystem, TypePackager):
    """provides a base class for qmake packages from any source"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("QMakePackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        QMakeBuildSystem.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)
