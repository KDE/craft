# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['3.99.5'] = "http://downloads.sourceforge.net/sourceforge/lame/lame-3.99.5.tar.gz"
        self.targetDigests['3.99.5'] = '03a0bfa85713adcc6b3383c12e2cc68a9cfbf4c4'
        self.targetInstSrc['3.99.5'] = "lame-3.99.5"
        self.defaultTarget = '3.99.5'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/msys"] = "default"


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.args = "--disable-static --enable-shared "
