# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None

    def setTargets(self):
        self.description = "pkg-config is a helper tool used when compiling applications and libraries"
        self.svnTargets["master"] = "git://anongit.freedesktop.org/pkg-config"
        for ver in ["0.26", "0.29.2"]:
            self.targets[ver] = f"https://pkg-config.freedesktop.org/releases/pkg-config-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"pkg-config-{ver}"
        self.targetDigests["0.29.2"] = (["6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.29.2"
        if CraftCore.compiler.isMinGW():
            self.patchToApply["0.29.2"] = [("mingw11.diff", 1)]


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--with-internal-glib", "PKG_CONFIG=:"]
        if not CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-with-libiconv=gnu"]
        else:
            # work around https://gitlab.freedesktop.org/pkg-config/pkg-config/-/issues/81
            self.subinfo.options.configure.cflags += "-Wno-int-conversion"
            self.subinfo.options.configure.cxxflags += "-Wno-int-conversion"

    def createPackage(self):
        # TODO: reduce package size
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        return super().createPackage(self)
