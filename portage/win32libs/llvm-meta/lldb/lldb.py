# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.patchToApply["4.0.1"] = [("lldb-4.0.1.src-20170821.diff", 1)]


    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/llvm-meta/llvm"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        if self.buildType().startswith("Rel"):
            # forcing build in Release mode, RelWithDebInfo would take lots of disk space (around 10 G) and memory during link
            options += ' -DCMAKE_BUILD_TYPE=Release'
        return options
