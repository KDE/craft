#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.AutoToolsBuildSystem import *
from Package.PackageBase import *
from Packager.TypePackager import *
from Source.MultiSource import *


class AutoToolsPackageBase(PackageBase, MultiSource, AutoToolsBuildSystem, TypePackager):
    """provides a base class for autotools based packages from any source"""

    def __init__(self):
        craftDebug.log.debug("AutoToolsPackageBase.__init__ called")
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        TypePackager.__init__(self)
        # needed to run autogen sh, this is needed in all checkouts but normaly not in a tarball
        if self.subinfo.hasSvnTarget():
            self.subinfo.options.configure.bootstrap = True
