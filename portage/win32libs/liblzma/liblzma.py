# -*- coding: utf-8 -*-

import os
import shutil

import info
import compiler


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '5.2.2'
        self.targets[ver] = 'http://tukaani.org/xz/xz-' + ver + '.tar.xz'
        self.targetInstSrc[ver] = 'xz-' + ver
        if not compiler.isMinGW():
            self.patchToApply[ver] = [('xz-5.0.5.diff', 1), ('xz-cmake-5.0.5.diff', 1)]
        self.targetDigests['5.0.5'] = '56f1d78117f0c32bbb1cfd40117aa7f55bee8765'

        self.shortDescription = "free general-purpose data compression software with high compression ratio"
        self.defaultTarget = ver

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


from Package.CMakePackageBase import *

class PackageCMake(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False

    def install( self ):
        if not AutoToolsPackageBase.install(self):
            return False
        utils.copyFile(os.path.join(self.imageDir(), "bin", "liblzma-5.dll"), os.path.join(self.imageDir(), "bin", "liblzma.dll"), False)
        return True

if compiler.isMinGW():
    class Package(PackageMSys): pass
else:
    class Package(PackageCMake): pass
