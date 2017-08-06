# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for branch in ["master", "release"]:
            self.svnTargets[branch] = "[git]git://cmake.org/cmake.git|%s" % branch
            self.targetInstallPath[branch] = os.path.join("dev-utils", "cmake-src")

        self.defaultTarget = "release"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DKWSYS_INSTALL_LIB_DIR=lib -DKWSYS_INSTALL_INCLUDE_DIR=include"

    def install(self):
        if not CMakePackageBase.install(self):
            return False
        for name in ["cmake", "cmake-gui", "cmcldeps", "cpack", "ctest"]:
            if not utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", f"{name}.exe"),
                                    os.path.join(self.imageDir(), "dev-utils", "cmake", "bin", f"{name}.exe")):
                return False
        return True
