import info
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        # We need this as a host tool. Craft at this point isn't set up to produce both
        # host and target binaries, so on Android we have host tools in the docker image.
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["1.16.1", "1.16.3"]:
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
        self.patchLevel["1.16.3"] = 1
        self.description = "Automake is a tool for automatically generating Makefile.in files compliant with the GNU Coding Standards."
        self.defaultTarget = "1.16.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/autoconf"] = None
        self.buildDependencies["dev-utils/perl"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared "

    def postInstall(self):
        return self.patchInstallPrefix(
            [
                os.path.join(self.installDir(), "bin", "aclocal"),
                os.path.join(self.installDir(), "bin", "aclocal-1.16"),
                os.path.join(self.installDir(), "bin", "automake"),
                os.path.join(self.installDir(), "bin", "automake-1.16"),
                os.path.join(self.installDir(), "share", "automake-1.16", "Automake/Config.pm"),
            ],
            self.subinfo.buildPrefix,
            CraftCore.standardDirs.craftRoot(),
        )
