import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Ki18n"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-util/gettext-tools"] = "default"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["libs/qttools"] = "default"
        self.runtimeDependencies["libs/qtscript"] = "default"
        self.runtimeDependencies["libs/qtdeclarative"] = "default"
        self.runtimeDependencies["win32libs/gettext"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
