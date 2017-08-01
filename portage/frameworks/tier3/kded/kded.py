import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Extensible deamon for providing system level services"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies['frameworks/kinit'] = "default"
        self.runtimeDependencies['frameworks/kconfig'] = "default"
        self.runtimeDependencies['frameworks/kcoreaddons'] = "default"
        self.runtimeDependencies['frameworks/kcrash'] = "default"
        self.runtimeDependencies['frameworks/kdbusaddons'] = "default"
        self.runtimeDependencies['frameworks/kdoctools'] = "default"
        self.runtimeDependencies['frameworks/kservice'] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
