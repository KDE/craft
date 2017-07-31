import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Grantlee Theme Editor"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/ktexteditor"] = "default"
        self.runtimeDependencies["frameworks/knewstuff"] = "default"
        self.runtimeDependencies["frameworks/karchive"] = "default"
        self.runtimeDependencies["frameworks/syntax-highlighting"] = "default"

        self.runtimeDependencies["kde/messagelib"] = "default"
        self.runtimeDependencies["kde/pimcommon"] = "default"
        self.runtimeDependencies["kde/grantleetheme"] = "default"
        self.runtimeDependencies["kde/akonadi-mime"] = "default"
        self.runtimeDependencies["kde/libkleo"] = "default"
        self.runtimeDependencies["kde/kimap"] = "default"
        self.runtimeDependencies["kde/kpimtextedit"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
