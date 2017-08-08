import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.description = 'kdevelop languages and other plugins'

    def setDependencies(self):
        self.runtimeDependencies["extragear/kdevelop/kdev-python"] = "default"
        self.runtimeDependencies["extragear/kdevelop/kdev-ruby"] = "default"
        self.runtimeDependencies["extragear/kdevelop/kdev-php"] = "default"
        self.runtimeDependencies['extragear/kdev-qmljs'] = 'default'


# self.runtimeDependencies['extragear/kdev-clang'] = 'default'


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
