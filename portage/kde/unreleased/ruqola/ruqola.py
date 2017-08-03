import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]kde:ruqola"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebsockets"] = "default"
        self.runtimeDependencies["libs/qt5/qtnetworkauth"] = "default"
        self.runtimeDependencies["frameworks/tier1/kirigami"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
