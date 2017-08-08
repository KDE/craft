import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]kde:kdiagram"
        self.defaultTarget = "master"

        self.description = "Powerful libraries (KChart, KGantt) for creating business diagrams"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
