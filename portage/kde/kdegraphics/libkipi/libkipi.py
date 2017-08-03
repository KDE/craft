# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["dev-util/gettext-tools"] = "default"
        self.runtimeDependencies["win32libs/expat"] = "default"
        self.runtimeDependencies["win32libs/tiff"] = "default"
        self.runtimeDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
