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
        self.description = "GNU libtool is a generic library support script."
        self.webpage = "https://www.gnu.org/software/libtool/ "
        self.releaseManagerId = 1741

        for ver in ["2.5.4"]:
            # self.targets[ver] = f"https://files.kde.org/craft/sources/dev-utils/libtool/libtool-{ver}.tar.xz"
            self.targets[ver] = f"https://ftpmirror.gnu.org/libtool/libtool-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libtool-{ver}"

        self.targetDigests["2.4.7"] = (
            ["da8ebb2ce4dcf46b90098daf962cffa68f4b4f62ea60f798d0ef12929ede6adf"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.defaultTarget = "2.5.4"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False

    def postInstall(self):
        return self.patchInstallPrefix(
            [(self.installDir() / x) for x in ["bin/libtool", "bin/libtoolize"]],
            self.subinfo.buildPrefix,
            CraftCore.standardDirs.craftRoot(),
        )
