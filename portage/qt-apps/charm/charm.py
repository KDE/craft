# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *

from EmergeOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/KDAB/Charm.git'
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = "The Cross-Platform Time Tracker"


    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['qt-libs/qtkeychain'] = 'default'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = " -DCHARM_PREPARE_DEPLOY=OFF "

