import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # We need this as a host tool. Craft at this point isn't set up to produce both
        # host and target binaries, so on Android we have host tools in the docker image.
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.description = "Automake is a tool for automatically generating Makefile.in files compliant with the GNU Coding Standards."
        self.webpage = "http://www.gnu.org/software/automake/"
        self.releaseManagerId = 144

        for ver in ["1.16.1", "1.16.3", "1.16.5", "1.18.1"]:
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
        self.targetDigests["1.18.1"] = (
            ["168aa363278351b89af56684448f525a5bce5079d0b6842bd910fdd3f1646887"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.patchLevel["1.16.3"] = 1
        self.defaultTarget = "1.18.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/autoconf"] = None
        self.buildDependencies["dev-utils/perl"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False

    def postInstall(self):
        major, minor, patch = self.subinfo.buildTarget.split(".")

        return self.patchInstallPrefix(
            [
                self.installDir() / "bin/aclocal",
                self.installDir() / f"bin/aclocal-{major}.{minor}",
                self.installDir() / "bin/automake",
                self.installDir() / f"bin/automake-{major}.{minor}",
                self.installDir() / f"share/automake-{major}.{minor}/Automake/Config.pm",
            ],
            self.subinfo.buildPrefix,
            CraftCore.standardDirs.craftRoot(),
        )
