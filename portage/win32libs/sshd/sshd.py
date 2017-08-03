# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.0.2'] = "http://officespace.kdab.com/~andy/CESSH-14454.zip"
        self.targetInstSrc['0.0.2'] = "SSH"
        self.patchToApply['0.0.2'] = ('SSH-20100512.diff', 1)
        self.defaultTarget = '0.0.2'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/openssl"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
