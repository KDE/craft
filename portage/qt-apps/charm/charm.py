# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *

from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/KDAB/Charm.git'
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = "The Cross-Platform Time Tracker"


    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['qt-libs/qtkeychain'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DCHARM_SIGN_INSTALLER=OFF"

    def createPackage(self):
        if craftSettings.getboolean("QtSDK", "Enabled", False):
            keychain = portage.getPackageInstance("qt-libs", "qtkeychain")
            utils.copyDir(keychain.imageDir(), os.path.join( craftSettings.get("QtSDK", "Path") , craftSettings.get("QtSDK", "Version"), craftSettings.get("QtSDK", "Compiler")))

        old = self.subinfo.options.make.makeOptions
        self.subinfo.options.make.makeOptions = "package"
        out = CMakePackageBase.make(self)
        self.subinfo.options.make.makeOptions = old
        return out
