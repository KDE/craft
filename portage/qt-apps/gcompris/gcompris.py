# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = '[git]kde:gcompris'
        self.defaultTarget = 'master'
        self.shortDescription = "GCompris is a high quality educational software suite comprising of numerous activities for children aged 2 to 10."


    def setDependencies( self ):
        self.runtimeDependencies['libs/qtbase'] = 'default'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DQt5_DIR=%s -DBUILD_STANDALONE=OFF" % CraftStandardDirs.craftRoot()