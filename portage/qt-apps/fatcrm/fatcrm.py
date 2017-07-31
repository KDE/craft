# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *

from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/FatCRM.git|frameworks"
        self.defaultTarget = "master"

        self.shortDescription = "Desktop Application for SugarCRM"
        self.homepage = "http://www.kdab.com/"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/kwallet"] = "default"
        self.runtimeDependencies["kde/akonadi"] = "default"
        self.runtimeDependencies["kde/kcontacts"] = "default"
        self.runtimeDependencies["kde/kcalcore"] = "default"
        self.runtimeDependencies["kde/akonadi-contacts"] = "default"
        self.runtimeDependencies["qt-libs/kdsoap"] = "default"
        self.runtimeDependencies["qt-libs/kdreports"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
