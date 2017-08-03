import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier1/kdbusaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier4/kdelibs4support"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier3/kdeclarative"] = "default"
        self.runtimeDependencies["frameworks/tier2/kpackage"] = "default"
        self.runtimeDependencies["frameworks/tier1/solid"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
