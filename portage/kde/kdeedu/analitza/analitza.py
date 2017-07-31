import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Analitza Library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"

        self.buildDependencies["win32libs/eigen3"] = "default"
        self.runtimeDependencies["win32libs/glew"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
