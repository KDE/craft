import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.shortDescription = 'kf5 tier1'

    def setDependencies(self):
        self.runtimeDependencies["frameworks/tier2/kauth"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcrash"] = "default"
        self.runtimeDependencies["frameworks/tier2/kdnssd"] = "default"
        self.runtimeDependencies["frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/tier2/kfilemetadata"] = "default"
        self.runtimeDependencies["frameworks/tier2/kjobwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier2/kpackage"] = "default"
        self.runtimeDependencies["frameworks/tier2/kunitconversion"] = "default"
        self.runtimeDependencies["frameworks/tier1/kirigami"] = "default"


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
