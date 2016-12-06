#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
from CraftDebug import craftDebug
from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.QMakeBuildSystem import *
from Packager.TypePackager import *

class QMakePackageBase (PackageBase, MultiSource, QMakeBuildSystem, TypePackager):
    """provides a base class for qmake packages from any source"""
    def __init__(self):
        craftDebug.log.debug("QMakePackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        QMakeBuildSystem.__init__(self)
        TypePackager.__init__(self)
