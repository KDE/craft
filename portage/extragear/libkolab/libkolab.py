# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.4.1', '0.5.0']:
            self.targets[ver] = 'http://git.kolab.org/libkolab/snapshot/libkolab-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = "libkolab-" + ver
        self.patchToApply['0.4.1'] = [("libkolab-fixes.diff", 1)]
        self.patchToApply['0.5.0'] = [("libkolab-0.5.0-fixes.diff", 1)]

        self.description = ''
        self.defaultTarget = '0.5.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["win32libs/libkolabxml"] = "default"

        # the following runtimeDependencies are dragged in by the static libkolabxml library
        self.runtimeDependencies["binary/xerces-c-bin"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-system"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-thread"] = "default"

        # this is a real dependency of libkolab
        self.runtimeDependencies['kde/kdepimlibs'] = 'default'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_TESTS=OFF"
