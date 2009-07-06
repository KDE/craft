# -*- coding: utf-8 -*-


from KDE4BuildSystem import *;
from CMakeBuildSystem import *;
from QMakeBuildSystem import *;
from AutoToolsBuildSystem import *;
from BinaryBuildSystem import *;

import info
import utils

def BuildSystemFactory(buildSystemType, source):
    """ return BuildSystemBase derived instance for recent settings"""
    utils.debug( "buildsystemFactory called", 1 )
    buildSystem = None

    if buildSystemType == 'cmake':
        buildSystem = CMakeBuildSystem()
    elif buildSystemType == 'kde4':
        buildSystem = KDE4BuildSystem()
    elif buildSystemType == 'qmake':
        buildSystem = QMakeBuildSystem()
    elif buildSystemType == 'autotools':
        buildSystem = AutoToolsBuildSystem()
    elif buildSystemType == 'binary':
        buildSystem = BinaryBuildSystem()
    else:   
        utils.die("none or unsupported buildsystem set, use self.buildSystemType='type', where type could be 'binary', 'cmake', 'qmake', 'autotools' or 'KDE4'")
        
    buildSystem.source = source
    buildSystem.subinfo = source.subinfo
    return buildSystem
