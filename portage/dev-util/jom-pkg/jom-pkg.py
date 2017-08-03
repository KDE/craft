# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        """ """
        self.svnTargets['svnHEAD'] = "git://qt.code.qt.io/qt-labs/jom.git"
        self.svnTargets['mingw'] = "git://gitorious.org/~saroengels/qt-labs/jom-mingw.git"
        self.svnTargets['cmake'] = "git://gitorious.org/~saroengels/qt-labs/jom-cmake.git"
        self.svnTargets['static'] = "git://qt.code.qt.io/qt-labs/jom.git"
        self.svnTargets['static-cmake'] = "git://gitorious.org/~saroengels/qt-labs/jom-cmake.git"
        self.targetSrcSuffix['cmake'] = "cmake"
        self.targetSrcSuffix['mingw'] = "mingw"

        self.defaultTarget = 'svnHEAD'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/msys"] = "default"
        self.buildDependencies["dev-util/qlalr"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DFLEX_EXECUTABLE=" + os.path.join(CraftStandardDirs.craftRoot(), "msys",
                                                                                  "bin",
                                                                                  "flex.exe") + " -DJOM_ENABLE_TESTS=ON"
        if self.buildTarget.startswith("static"):
            self.subinfo.options.configure.args += " -DQT_QMAKE_EXECUTABLE=" + os.path.join(
                CraftStandardDirs.craftRoot(), "qt-static", "bin", "qmake.exe")
