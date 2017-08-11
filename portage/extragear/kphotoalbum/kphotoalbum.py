# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:kphotoalbum.git'

        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["kde/kdegraphics/kipi-plugins"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
