# -*- coding: utf-8 -*-
import io

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        # TODO support for cross-compiling to Android not implemented here yet
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Native

    def setTargets(self):
        for ver in ["71.1", "74.1", "74.2"]:
            major, minor = ver.split(".")
            self.targets[ver] = f"https://github.com/unicode-org/icu/releases/download/release-{major}-{minor}/icu4c-{major}_{minor}-src.tgz"
            self.targetInstSrc[ver] = os.path.join("icu", "source")
        self.targetDigests["71.1"] = (["67a7e6e51f61faf1306b6935333e13b2c48abd8da6d2f46ce6adca24b1e21ebf"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["74.1"] = (["86ce8e60681972e60e4dcb2490c697463fcec60dd400a5f9bffba26d0b52b8d0"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["74.2"] = (["68db082212a96d6f53e35d60f47d38b962e9f9d207a74cfac78029ae8ff5e08c"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["71.1"] = [("icu-71.1-20221112.diff", 1)]
        self.patchToApply["74.1"] = [("icu-71.1-20221112.diff", 1)]
        self.patchToApply["74.2"] = [("icu-71.1-20221112.diff", 1)]
        self.defaultTarget = "74.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += [
            "--disable-samples",
            "--disable-tests",
            "--enable-debug=no",
            "--enable-release=yes",
            "--enable-static=no",
            "--enable-shared=yes",
        ]
        if CraftCore.compiler.platform.isWindows:
            self.subinfo.options.configure.args += ["--with-data-packaging=dll"]
            if CraftCore.compiler.isMSVC():
                self.subinfo.options.configure.args += ["--enable-extras=no"]

    def make(self):
        utils.createDir(Path(self.buildDir()) / "data/out/tmp/")
        f = open(Path(self.buildDir()) / "data/out/tmp/dirs.timestamp", "w")
        f.write("timestamp")
        f.close()
        # ensure TARGET is not set, else the build system will try to build its content and fail
        with utils.ScopedEnv({"TARGET": None}):
            return super().make()

    def install(self):
        # ensure TARGET is not set, else the build system will try to build its content and fail
        with utils.ScopedEnv({"TARGET": None}):
            if not super().install():
                return False
        if CraftCore.compiler.isMSVC():
            files = os.listdir(os.path.join(self.installDir(), "lib"))
            for dll in files:
                if dll.endswith(".dll"):
                    utils.moveFile(os.path.join(self.installDir(), "lib", dll), os.path.join(self.installDir(), "bin", dll))
        return True

    def postInstall(self):
        res = True
        path = os.path.join(self.installDir(), "bin/icu-config")
        if os.path.exists(path):
            res = self.patchInstallPrefix([path], self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())
        return res
