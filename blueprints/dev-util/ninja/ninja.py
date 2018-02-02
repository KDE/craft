# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        """ """
        self.svnTargets['master'] = "https://github.com/martine/ninja.git"
        for ver in ["1.6.0", "1.7.1", "1.7.2", "1.8.2"]:
            self.targets[ver] = f"https://github.com/ninja-build/ninja/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"ninja-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ninja-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests['1.6.0'] = 'a6ff055691f6d355234298c21cc18961b4ca2ed9'
        self.targetDigests['1.7.2'] = (['2edda0a5421ace3cf428309211270772dd35a91af60c96f93f90df6bc41b16d9'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.8.2'] = (['86b8700c3d0880c2b44c2ff67ce42774aaf8c28cbf57725cb881569288c1c6f4'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.8.2"

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
        if CraftCore.compiler.isMinGW():
            command += " --platform=mingw"
        return utils.system(command)

    def install(self):
        utils.copyFile(os.path.join(self.sourceDir(), "ninja.exe"), os.path.join(self.installDir(), "bin", "ninja.exe"))
        return True
