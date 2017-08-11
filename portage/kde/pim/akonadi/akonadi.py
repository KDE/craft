# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.patchToApply["17.04.0"] = [("akonadi-17.04.0-20170530.diff", 1)]
        self.patchToApply["17.04.1"] = [("akonadi-17.04.0-20170530.diff", 1)]
        self.patchToApply["17.04.2"] = [("akonadi-17.04.0-20170530.diff", 1)]

        self.description = "A storage service for PIM data and meta data"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/boost/boost-headers"] = "default"
        self.runtimeDependencies["win32libs/libxslt"] = "default"
        self.runtimeDependencies["win32libs/sqlite"] = "default"
        self.runtimeDependencies["win32libs/shared-mime-info"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier3/kdesignerplugin"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = ""
        if not self.subinfo.options.isActive("binary/mysql"):
            self.subinfo.options.configure.args += " -DDATABASE_BACKEND=SQLITE "
