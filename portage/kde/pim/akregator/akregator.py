import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Akregator"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/kcrash"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/kcmutils"] = "default"
        self.runtimeDependencies["frameworks/knotifications"] = "default"
        self.runtimeDependencies["frameworks/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/kparts"] = "default"
        self.runtimeDependencies["frameworks/ktexteditor"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/kdbusaddons"] = "default"

        self.runtimeDependencies["kde/grantleetheme"] = "default"
        self.runtimeDependencies["kde/kontactinterface"] = "default"
        self.runtimeDependencies["kde/libkdepim"] = "default"
        self.runtimeDependencies["kde/libkleo"] = "default"
        self.runtimeDependencies["kde/messagelib"] = "default"
        self.runtimeDependencies["kde/syndication"] = "default"
        self.runtimeDependencies["kde/akonadi-mime"] = "default"
        self.runtimeDependencies["kde/pimcommon"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
