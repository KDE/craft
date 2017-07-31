import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Calendar Utils library"
        self.patchToApply['17.04.1'] = [("fix-kcalutils.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = "default"
        self.runtimeDependencies["frameworks/kdelibs4support"] = "default"
        self.runtimeDependencies["frameworks/kcodecs"] = "default"
        self.runtimeDependencies["kde/kcalcore"] = "default"
        self.runtimeDependencies["kdesupport/grantlee"] = "default"
        self.runtimeDependencies["kde/kidentitymanagement"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
