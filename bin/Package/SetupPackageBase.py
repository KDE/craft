#
# copyright (c) 2011 Ralf Habacker <ralf.habacker@freenet.de>
#

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.BuildSystemBase import *
from Packager.PackagerBase import *

class SetupPackageBase (PackageBase, MultiSource, BuildSystemBase, PackagerBase):
    """provides a base class for 3rd party installers or msi packages"""
    def __init__(self):
        utils.debug("SetupPackageBase.__init__ called", 2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        BuildSystemBase.__init__(self)
        PackagerBase.__init__(self)
        self.subinfo.options.unpack.runInstaller = True