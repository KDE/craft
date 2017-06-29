# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *

from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets["master"] = "https://github.com/KDAB/FatCRM.git|frameworks"
        self.defaultTarget = "master"

        self.shortDescription = "Desktop Application for SugarCRM"
        self.homepage = "http://www.kdab.com/"


    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kwallet"] = "default"
        self.dependencies["kde/akonadi"] = "default"
        self.dependencies["kde/kcontacts"] = "default"
        self.dependencies["kde/kcalcore"] = "default"
        self.dependencies["kde/akonadi-contacts"] = "default"
        self.dependencies["qt-libs/kdsoap"] = "default"
        self.dependencies["qt-libs/kdreports"] = "default"


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DCHARM_SIGN_INSTALLER=OFF"

    def createPackage(self):
        if craftSettings.getboolean("QtSDK", "Enabled", False):
            # windeployqt tries to deploy every lib starting with qt5....
            # therefore we need to make sure it can find qt5keychain
            keychain = portage.getPackageInstance("qt-libs", "qtkeychain")
            utils.copyDir(keychain.imageDir(), os.path.join( craftSettings.get("QtSDK", "Path") , craftSettings.get("QtSDK", "Version"), craftSettings.get("QtSDK", "Compiler")))

        old = self.subinfo.options.make.makeOptions
        self.subinfo.options.make.makeOptions = "package"
        out = CMakePackageBase.make(self)
        self.subinfo.options.make.makeOptions = old
        return out
