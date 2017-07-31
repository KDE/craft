import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Crypto library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = "default"
        self.runtimeDependencies["frameworks/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/kcodecs"] = "default"
        self.runtimeDependencies["frameworks/kitemmodels"] = "default"
        self.runtimeDependencies["kde/kpimtextedit"] = "default"
        self.runtimeDependencies["win32libs/gpgme"] = "default"
        self.runtimeDependencies["win32libs/boost"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
