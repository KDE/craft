import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Calendar Tools"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["kde/akonadi"] = "default"
        self.runtimeDependencies["kde/kcalcore"] = "default"
        self.runtimeDependencies["kde/kcalutils"] = "default"
        self.runtimeDependencies["kde/akonadi-calendar"] = "default"
        self.runtimeDependencies["kde/libkdepim"] = "default"
        self.runtimeDependencies["kde/calendarsupport"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
