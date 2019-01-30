# -*- coding: utf-8 -*-

import sys

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        """ """
        self.svnTargets['master'] = "https://github.com/martine/ninja.git"

        for ver in ["1.6.0", "1.7.1", "1.7.2", "1.8.2", "1.9.0"]:
            self.targets[ver] = f"https://github.com/ninja-build/ninja/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"ninja-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ninja-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests['1.6.0'] = 'a6ff055691f6d355234298c21cc18961b4ca2ed9'
        self.targetDigests['1.7.2'] = (['2edda0a5421ace3cf428309211270772dd35a91af60c96f93f90df6bc41b16d9'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.8.2'] = (['86b8700c3d0880c2b44c2ff67ce42774aaf8c28cbf57725cb881569288c1c6f4'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.9.0'] = (['5d7ec75828f8d3fd1a0c2f31b5b0cea780cdfe1031359228c428c1a48bfcd5b9'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.9.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/mingw-w64"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def configure(self):
        return True

    def make(self):
        self.enterSourceDir()
        command = [sys.executable, "configure.py", "--bootstrap"]
        if CraftCore.compiler.isMinGW():
            command += ["--platform=mingw"]
        return utils.system(command)

    def install(self):
        utils.copyFile(os.path.join(self.sourceDir(), f"ninja{CraftCore.compiler.executableSuffix}"), os.path.join(self.installDir(), "bin", f"ninja{CraftCore.compiler.executableSuffix}"))
        return True
