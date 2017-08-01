import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]kde:ruqola"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies['virtual/base'] = 'default'
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["libs/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qtwebsockets"] = "default"
        self.runtimeDependencies["libs/qtnetworkauth"] = "default"
        self.runtimeDependencies["frameworks/kirigami"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
