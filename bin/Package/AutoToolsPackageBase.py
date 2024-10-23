#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#
from BuildSystem.AutoToolsBuildSystem import AutoToolsBuildSystem
from CraftCore import CraftCore
from Package.PackageBase import PackageBase
from Packager.TypePackager import TypePackager
from Source.MultiSource import MultiSource


class AutoToolsPackageBase(PackageBase, MultiSource, AutoToolsBuildSystem, TypePackager):
    """provides a base class for autotools based packages from any source"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("AutoToolsPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        AutoToolsBuildSystem.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)
        # needed to run autogen sh, this is needed in all checkouts but normaly not in a tarball
        if self.subinfo.hasSvnTarget():
            self.subinfo.options.configure.bootstrap = True
