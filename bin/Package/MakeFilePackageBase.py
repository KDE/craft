# 
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

from PackageBase import *;
from Source.MultiSource import *;
from BuildSystem.MakeFileBuildSystem import *;
from Packager.KDEWinPackager import *;

class MakeFilePackageBase (PackageBase, MultiSource, MakeFileBuildSystem, KDEWinPackager):
    """provides a base class for simple makefile based packages from any source"""
    def __init__(self):
        utils.debug("MakeFilePackageBase.__init__ called",2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        MakeFileBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
