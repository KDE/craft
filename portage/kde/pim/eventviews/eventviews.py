import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Evenviews library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcodecs"] = "default"
        self.runtimeDependencies["kde/pim/kcalutils"] = "default"
        self.runtimeDependencies["kde/pim/kcalcore"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-calendar"] = "default"
        self.runtimeDependencies["kde/pim/kmime"] = "default"
        self.runtimeDependencies["kde/pim/calendarsupport"] = "default"
        self.runtimeDependencies["extragear/kdiagram"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
