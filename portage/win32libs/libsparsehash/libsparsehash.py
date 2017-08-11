# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['2.0.2'] = "https://sparsehash.googlecode.com/files/sparsehash-2.0.2.tar.gz"
        self.targetInstSrc['2.0.2'] = "sparsehash-2.0.2"
        self.targetDigests['2.0.2'] = '12c7552400b3e20464b3362286653fc17366643e'

        self.description = "An extremely memory-efficient hash_map implementation."
        self.webpage = "http://code.google.com/p/sparsehash/"
        self.defaultTarget = '2.0.2'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/msys"] = "default"


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--disable-static --enable-shared "
