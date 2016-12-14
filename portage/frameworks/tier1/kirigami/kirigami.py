import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:kirigami|master'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qtgraphicaleffects"] = "default"
        self.dependencies["libs/qtquickcontrols"] = "default"
        self.dependencies["frameworks/kdeclarative"] = "default"

from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DDESKTOP_ENABLED=ON '
