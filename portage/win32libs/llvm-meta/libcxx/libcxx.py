# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.targetDigests['3.7.0'] = '73adf9fdca5086dd47a32b34a398d2c1d492d18e'

        for ver in self.svnTargets.keys() | self.targets.keys():
            self.patchToApply[ver] = [("fix_shortpath.patch", 1), ("0041-libcxx-add-support-for-mingw-w64.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/llvm-meta/clang"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = '-DCMAKE_CXX_FLAGS="-D_LIBCPP_HAS_NO_CONSTEXPR" -DLIBCXX_ENABLE_SHARED=OFF '

    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        if self.buildType().startswith("Rel"):
            # forcing build in Release mode, RelWithDebInfo would take lots of disk space and memory during link
            options += ' -DCMAKE_BUILD_TYPE=Release '
        return options
