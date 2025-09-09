# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash
from Utils.Arguments import Arguments


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = ~CraftCore.compiler.Platforms.Android

    def setTargets(self):
        for ver in ["1.3", "1.3.1"]:
            self.targets[ver] = f"https://www.zlib.net/zlib-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"zlib-{ver}"
        self.patchToApply["1.3"] = [
            ("zlib-1.2.12-20220404.diff", 1),
            (
                # don't conditonlessly define Z_HAVE_UNISTD_H
                "zlib-1.2.12-20220503.diff",
                1,
            ),
        ]
        self.patchToApply["1.3.1"] = [
            ("zlib-1.2.12-20220404.diff", 1),
            (
                # don't conditonlessly define Z_HAVE_UNISTD_H
                "zlib-1.2.12-20220503.diff",
                1,
            ),
            # use the same dll name with mingw and msvc
            # this allows using zlib in prebuilt libraries like gpg
            ("zlib-1.3.1-20240818.diff", 1),
        ]

        self.targetDigests["1.3"] = (
            ["8a9ba2898e1d0d774eca6ba5b4627a11e5588ba85c8851336eb38de4683050a7"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.3.1"] = (
            ["38ef96b8dfe510d42707d9c781877914792541133e1870841463bfa73f883e32"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.description = "The zlib compression and decompression library"
        self.webpage = "https://www.zlib.net"
        self.defaultTarget = "1.3.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.platform.isWindows:

    class Package(CMakePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.args += [f"-DINSTALL_PKGCONFIG_DIR={CraftCore.standardDirs.craftRoot() / 'lib/pkgconfig'}"]

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.autoreconf = False
            self.subinfo.options.configure.noCacheFile = True
            if self.subinfo.options.dynamic.buildStatic:
                self.subinfo.options.configure.staticArgs = Arguments(["--static"])
            else:
                self.subinfo.options.configure.staticArgs = Arguments(["--shared"])
            self.supportsCCACHE = False
            self.platform = ""
