#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import EmergeDebug
from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.CMakeBuildSystem import *
from Packager.TypePackager import *

class CMakePackageBase (PackageBase, MultiSource, CMakeBuildSystem, TypePackager):
    """provides a base class for cmake packages from any source"""
    def __init__(self):
        EmergeDebug.debug("CMakePackageBase.__init__ called", 2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        CMakeBuildSystem.__init__(self)
        TypePackager.__init__(self)
