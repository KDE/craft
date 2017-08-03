import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.shortDescription = 'kf5 tier4'

    def setDependencies(self):
        self.runtimeDependencies["frameworks/tier4/kdelibs4support"] = "default"
        self.runtimeDependencies["frameworks/tier4/frameworkintegration"] = "default"


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
