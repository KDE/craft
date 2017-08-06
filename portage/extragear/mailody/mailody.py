# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/pim/mailody'
        self.defaultTarget = 'svnHEAD'

    def setDependencies(self):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.runtimeDependencies['kde/kdepimlibs'] = 'default'
        self.runtimeDependencies["kde/kdeedu/analitza"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
