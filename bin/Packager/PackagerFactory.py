#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Packager.KDEWinPackager import *
from Packager.CPackPackager import *
from Packager.SevenZipPackager import *
from Packager.MSInstallerPackager import *
from Packager.InnoSetupPackager import *

def init(packager, parent):
    packager.subinfo = parent.subinfo
    packager.parent = parent
    packager.category = parent.category
    packager.package = parent.package
    packager.version = parent.version
    packager.buildTarget = parent.subinfo.buildTarget
    packager.PV = parent.PV
    return

def PackagerFactory(parent, packagerType):
    """provides multi packager type api
    return PackagerBase derived instance for recent settings"""
    utils.debug( "PackagerFactory called", 2 )
    packagers = []

    if packagerType:
        for packagerClass in packagerType:
            if not isinstance(packagerClass, PackagerBase):
                utils.die("PackagerFactory: unsupported packager %s" % packagerClass)
            else:
                packager = packagerClass()
                init(packager, parent)
                packagers.append(packager)
    else:
        # automatic detection
        packager = InnoSetupPackager()
        init(packager, parent)

        if packager.configFile() != None:
            packagers.append(packager)

        # default packager
        if len(packagers) == 0:
            packager = KDEWinPackager()
            init(packager, parent)
            packagers.append(packager)
    return packagers

