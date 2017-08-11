# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/FatCRM.git|frameworks"
        self.defaultTarget = "master"

        self.description = "Desktop Application for SugarCRM"
        self.webpage = "http://www.kdab.com/"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["kde/pim/akonadi"] = "default"
        self.runtimeDependencies["kde/pim/kcontacts"] = "default"
        self.runtimeDependencies["kde/pim/kcalcore"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = "default"
        self.runtimeDependencies["qt-libs/kdsoap"] = "default"
        self.runtimeDependencies["qt-libs/kdreports"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
