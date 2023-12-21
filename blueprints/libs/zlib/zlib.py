# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["1.3"]:
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
        self.targetDigests["1.3"] = (
            ["8a9ba2898e1d0d774eca6ba5b4627a11e5588ba85c8851336eb38de4683050a7"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.description = "The zlib compression and decompression library"
        self.webpage = "https://www.zlib.net"
        self.defaultTarget = "1.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isWindows:

    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
            self.subinfo.options.configure.args += [f"-DINSTALL_PKGCONFIG_DIR={CraftCore.standardDirs.craftRoot() / 'lib/pkgconfig'}"]

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.autoreconf = False
            self.subinfo.options.configure.noCacheFile = True
            self.supportsCCACHE = False
            self.platform = ""
