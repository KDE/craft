import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.16.1", "1.16.3", "1.16.5"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/automake/automake-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"automake-{ver}"

        self.targetDigests["1.16.1"] = (
            ["5d05bb38a23fd3312b10aea93840feec685bdf4a41146e78882848165d3ae921"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.16.3"] = (
            ["ff2bf7656c4d1c6fdda3b8bebb21f09153a736bcba169aaf65eab25fa113bf3a"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.targetDigests["1.16.5"] = (
            ["f01d58cd6d9d77fbdca9eb4bbd5ead1988228fdb73d6f7a201f5f8d6b118b469"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.patchLevel["1.16.3"] = 1
        self.description = "Automake is a tool for automatically generating Makefile.in files compliant with the GNU Coding Standards."
        self.defaultTarget = "1.16.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/autoconf"] = None
        self.buildDependencies["dev-utils/perl"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False

    def postInstall(self):
        return self.patchInstallPrefix(
            [
                self.installDir() / "bin/aclocal",
                self.installDir() / "bin/aclocal-1.16",
                self.installDir() / "bin/automake",
                self.installDir() / "bin/automake-1.16",
                self.installDir() / "share/automake-1.16/Automake/Config.pm",
            ],
            self.subinfo.buildPrefix,
            CraftCore.standardDirs.craftRoot(),
        )
