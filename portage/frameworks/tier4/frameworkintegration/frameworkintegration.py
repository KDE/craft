import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = 'default'
        self.runtimeDependencies["frameworks/ki18n"] = 'default'
        self.runtimeDependencies["frameworks/kiconthemes"] = 'default'
        self.runtimeDependencies["frameworks/kio"] = 'default'
        self.runtimeDependencies["frameworks/knotifications"] = 'default'
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
