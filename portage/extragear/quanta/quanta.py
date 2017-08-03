import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://gitorious.org/kdevelop/quanta.git'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.runtimeDependencies["extragear/kdevelop/kdevplatform"] = "default"
        self.runtimeDependencies["extragear/kdevelop/kdev-php"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
