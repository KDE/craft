import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:yakuake'
        self.description = "a drop-down terminal emulator based on KDE Konsole technology"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.runtimeDependencies['kdeapps/konsole'] = 'default'


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
