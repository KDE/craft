import info


# deprecated class
class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:libkface'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["kdesupport/libface"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
