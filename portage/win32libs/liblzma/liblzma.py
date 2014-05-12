# -*- coding: utf-8 -*-

import os
import shutil

import info
import compiler


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '5.0.5'
        self.targets[ver] = 'http://tukaani.org/xz/xz-' + ver + '.tar.xz'
        self.targetInstSrc[ver] = 'xz-' + ver
        self.patchToApply[ver] = [('xz-5.0.5.diff', 1), ('xz-cmake-5.0.5.diff', 1)]
        self.targetDigests['5.0.5'] = '56f1d78117f0c32bbb1cfd40117aa7f55bee8765'

        self.shortDescription = "free general-purpose data compression software with high compression ratio"
        self.defaultTarget = ver

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
