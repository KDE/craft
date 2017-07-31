import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "KAddressBook"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/kdbusaddons"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/kcmutils"] = "default"
        self.runtimeDependencies["frameworks/kcrash"] = "default"
        self.runtimeDependencies["kde/libkleo"] = "default"
        self.runtimeDependencies["kde/akonadi"] = "default"
        self.runtimeDependencies["kde/kontactinterface"] = "default"
        self.runtimeDependencies["kde/libkdepim"] = "default"
        self.runtimeDependencies["kde/pimcommon"] = "default"
        self.runtimeDependencies["kde/grantleetheme"] = "default"
        self.runtimeDependencies["kde/kdepim-apps-libs"] = "default"
        self.runtimeDependencies["kde/akonadi-search"] = "default"
        self.runtimeDependencies["win32libs/gpgme"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
