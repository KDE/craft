# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['3.2.5']:
            self.targets[ver] = 'http://bitbucket.org/eigen/eigen/get/%s.tar.bz2' % ver
            self.archiveNames[ver] = "eigen-%s.tar.bz2" % ver
        self.targetInstSrc['3.2.5'] = 'eigen-eigen-bdd17ee3b1b3'
        self.targetDigests['3.2.5'] = 'aa4667f0b134f5688c5dff5f03335d9a19aa9b3d'
        self.patchToApply['3.2.5'] = [('eigen-3.2.5.tar-20160526.diff', 1)]

        self.description = 'C++ template library for linear algebra'
        self.defaultTarget = '3.2.5'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if craftCompiler.isMSVC():
            self.subinfo.options.configure.args = "-DBUILD_TESTS=OFF"
