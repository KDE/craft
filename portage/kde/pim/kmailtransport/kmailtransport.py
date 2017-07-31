import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Mailtransport library"
        self.patchToApply['17.04.1'] = [("fix-kmailtransport.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = "default"
        self.runtimeDependencies["frameworks/kwallet"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"
        self.runtimeDependencies["kde/kmime"] = "default"
        self.runtimeDependencies["kde/akonadi"] = "default"
        self.runtimeDependencies["kde/akonadi-mime"] = "default"
        self.runtimeDependencies['win32libs/cyrus-sasl'] = 'default'
        self.runtimeDependencies["frameworks/kcmutils"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
