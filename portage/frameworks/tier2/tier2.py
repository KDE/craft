import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.shortDescription = 'kf5 tier1'

    def setDependencies(self):
        self.runtimeDependencies['frameworks/kauth'] = 'default'
        self.runtimeDependencies['frameworks/kcompletion'] = 'default'
        self.runtimeDependencies['frameworks/kcrash'] = 'default'
        self.runtimeDependencies['frameworks/kdnssd'] = 'default'
        self.runtimeDependencies['frameworks/kdoctools'] = 'default'
        self.runtimeDependencies['frameworks/kfilemetadata'] = 'default'
        self.runtimeDependencies['frameworks/kjobwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kpackage'] = 'default'
        self.runtimeDependencies['frameworks/kunitconversion'] = 'default'
        self.runtimeDependencies['frameworks/kirigami'] = 'default'


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
