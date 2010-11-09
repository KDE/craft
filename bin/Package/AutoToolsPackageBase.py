# 
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

from PackageBase import *;
from Source.MultiSource import *;
from BuildSystem.AutoToolsBuildSystem import *;
from Packager.KDEWinPackager import *;

class AutoToolsPackageBase (PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    """provides a base class for autotools based packages from any source"""
    def __init__(self):
        utils.debug("AutoToolsPackageBase.__init__ called",2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)
        #needed to run autogen sh, this is needed in all checkouts but normaly not in a tarball
        if self.subinfo.hasSvnTarget():
            self.subinfo.options.configure.bootstrap = True
