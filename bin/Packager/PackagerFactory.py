# -*- coding: utf-8 -*-

from KDEWinPackager import *;
from CPackPackager import *;
from MSInstallerPackager import *;

import info
import utils

def PackagerFactory(packagerType, buildSystem):
    """ return PackagerBased derived instance """
    utils.debug( "PackagerFactory called", 1 )

    packager = None
    if packagerType == 'KDEWin' or packagerType == 'kdewin' or packagerType == None:
        packager = KDEWinPackager()
    elif packagerType == 'CPack':
        packager = CPackPackager()
    else:
        utils.die("none or unsupported packager set, use self.packagerType='type', where type could be 'KDEWin'")

    packager.subinfo = buildSystem.subinfo
    packager.buildSystem = buildSystem
    packager.source = buildSystem.source
    return packager
