import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["1.0.8"] = "https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz"
        self.targetInstSrc["1.0.8"] = "bzip2-1.0.8"
        self.targetDigests["1.0.8"] = (["ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.0.8"] = [(".files/fix-import-export-macros.patch", 1)]
        self.description = "shared libraries for handling bzip2 archives (runtime)"
        self.defaultTarget = "1.0.8"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBZIP2_SKIP_TOOLS=OFF"]

    def unpack(self):
        if not super().unpack():
            return False
        return utils.copyFile(self.blueprintDir() / ".files/CMakeLists.txt", self.sourceDir() / "CMakeLists.txt")

    def install(self):
        if not super().install():
            return False

        # Install bunzip2 symlink to bzip2, the behavior is altered in bzip2.c code by checking the program name.
        # See https://gitlab.com/bzip2/bzip2/-/blob/master/CMakeLists.txt?ref_type=heads#L378
        # We do it here be cause it is easier than to hack our CMake patch further.
        # CMake support has been added upstream and hopefully we can drop it all together ones version 1.1 is out
        linkSource = self.imageDir() / "bin" / f"bzip2{CraftCore.compiler.executableSuffix}"
        linkTarget = self.imageDir() / "bin" / f"bunzip2{CraftCore.compiler.executableSuffix}"
        if not utils.createShim(linkTarget, linkSource, keepArgv0=True):
            return False

        bzname = "bz2"
        if self.buildType() == "Debug":
            bzname = "libbz2"
        if not utils.configureFile(
            self.blueprintDir() / ".files/bzip2.pc.in",
            self.imageDir() / "lib/pkgconfig/bzip2.pc",
            {"bzname": bzname, "BZIP2_PREFIX": self.installPrefix(), "VERSION": self.buildTarget},
        ):
            return False
        return True
