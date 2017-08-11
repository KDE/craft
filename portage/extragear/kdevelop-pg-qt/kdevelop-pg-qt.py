import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['2.0'] = '[git]kde:kdevelop-pg-qt|2.0'
        self.defaultTarget = '2.0'

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
