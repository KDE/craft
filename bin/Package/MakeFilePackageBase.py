#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.MakeFileBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import *
from Source.MultiSource import *


class MakeFilePackageBase(PackageBase, MultiSource, MakeFileBuildSystem, TypePackager):
    """provides a base class for simple makefile based packages from any source"""

    def __init__(self):
        craftDebug.log.debug("MakeFilePackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        MakeFileBuildSystem.__init__(self)
        TypePackager.__init__(self)
