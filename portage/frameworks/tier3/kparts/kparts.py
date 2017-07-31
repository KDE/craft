import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Plugin framework for user interface components"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = "default"
        self.runtimeDependencies["frameworks/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"
        self.runtimeDependencies["frameworks/kjobwidgets"] = "default"
        self.runtimeDependencies["frameworks/kservice"] = "default"
        self.runtimeDependencies["frameworks/ktextwidgets"] = "default"
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
