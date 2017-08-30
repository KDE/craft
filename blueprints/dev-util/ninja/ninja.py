# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        """ """
        self.svnTargets['master'] = "https://github.com/martine/ninja.git"
        for ver in ["1.6.0", "1.7.1", "1.7.2"]:
            self.targets[ver] = "https://github.com/martine/ninja/archive/v%s.tar.gz" % ver
            self.archiveNames[ver] = "ninja-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "ninja-%s" % ver
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests['1.6.0'] = 'a6ff055691f6d355234298c21cc18961b4ca2ed9'
        self.targetDigests['1.7.2'] = (
            ['2edda0a5421ace3cf428309211270772dd35a91af60c96f93f90df6bc41b16d9'], CraftHash.HashAlgorithm.SHA256)

        # unconditionally use master for now, to fix:
        # https://github.com/ninja-build/ninja/issues/1161
        self.defaultTarget = "master" # TODO: Use 1.7.3 once released
        if craftCompiler.isMSVC2017():
            self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/python3"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def configure(self):
        return True

    def make(self):
        self.enterSourceDir()
        command = "python3 configure.py --bootstrap"
        if craftCompiler.isMinGW():
            command += " --platform=mingw"
        print(command)
        return self.system(command, "make")

    def install(self):
        utils.copyFile(os.path.join(self.sourceDir(), "ninja.exe"), os.path.join(self.installDir(), "bin", "ninja.exe"))
        return True
