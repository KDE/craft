import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Parallelized query system"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies['frameworks/kconfig'] = "default"
        self.runtimeDependencies['frameworks/kcoreaddons'] = "default"
        self.runtimeDependencies['frameworks/ki18n'] = "default"
        self.runtimeDependencies['frameworks/kio'] = "default"
        self.runtimeDependencies['frameworks/kservice'] = "default"
        self.runtimeDependencies['frameworks/plasma-framework'] = "default"
        self.runtimeDependencies['frameworks/solid'] = "default"
        self.runtimeDependencies['frameworks/threadweaver'] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
