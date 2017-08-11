import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:kwebkitpart'
        self.description = 'A WebKit browser component for KDE (KPart)'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['kde/kdelibs'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
