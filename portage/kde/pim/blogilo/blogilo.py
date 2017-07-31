import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Blogilo"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kcrash"] = "default"
        self.runtimeDependencies["frameworks/kdbusaddons"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/kwallet"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/syntax-highlighting"] = "default"

        self.runtimeDependencies["kde/kblog"] = "default"
        self.runtimeDependencies["kde/pimcommon"] = "default"
        self.runtimeDependencies["kde/kpimtextedit"] = "default"
        self.runtimeDependencies["kde/messagelib"] = "default"
        self.runtimeDependencies["kde/kimap"] = "default"
        self.runtimeDependencies["kde/libkgapi"] = "default"
        self.runtimeDependencies['libs/qtwebengine'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
