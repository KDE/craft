import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.description = 'kf5 tier1'

    def setDependencies(self):
        self.runtimeDependencies["frameworks/tier1/attica"] = "default"
        self.runtimeDependencies["frameworks/tier1/karchive"] = "default"
        # kapidox doesn't work as we are not tied to a python interpreter / library
        # self.runtimeDependencies["frameworks/tier1/kapidox"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcodecs"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kdbusaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier1/kidletime"] = "default"
        self.runtimeDependencies["frameworks/tier1/kimageformats"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemviews"] = "default"
        self.runtimeDependencies["frameworks/tier1/kplotting"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["frameworks/tier1/solid"] = "default"
        self.runtimeDependencies["frameworks/tier1/sonnet"] = "default"
        self.runtimeDependencies["frameworks/tier1/threadweaver"] = "default"
        self.runtimeDependencies["frameworks/tier1/breeze-icons"] = "default"


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
