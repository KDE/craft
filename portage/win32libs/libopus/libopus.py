# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.0.3'] = "http://downloads.xiph.org/releases/opus/opus-1.0.3.tar.gz"
        self.targets['1.1'] = "http://downloads.xiph.org/releases/opus/opus-1.1.tar.gz"
        self.targetDigests['1.0.3'] = '5781bdd009943deb55a742ac99db20a0d4e89c1e'
        self.targetDigests['1.1'] = '35005f5549e2583f5770590135984dcfce6f3d58'
        self.targetInstSrc['1.0.3'] = "opus-1.0.3"
        self.targetInstSrc['1.1'] = "opus-1.1"

        self.description = "Opus codec library"
        self.defaultTarget = '1.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/msys"] = "default"


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.args = "--disable-static --enable-shared --disable-doc"
