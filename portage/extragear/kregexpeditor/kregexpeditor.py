# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:kregexpeditor'
        self.description = "a regular expression editor for KDE"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
