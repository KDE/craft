import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        # self.targets['1.0.6'] = 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz'
        self.targets["1.0.6"] = "https://ftp.osuosl.org/pub/clfs/conglomeration/bzip2/bzip2-1.0.6.tar.gz"
        self.targetInstSrc["1.0.6"] = "bzip2-1.0.6"
        self.patchToApply["1.0.6"] = [("bzip.diff", 1), ("libbzip2-1.0.6-20210422.diff", 1)]
        self.targetDigests["1.0.6"] = "3f89f861209ce81a6bab1fd1998c0ef311712002"
        self.description = "shared libraries for handling bzip2 archives (runtime)"
        self.patchLevel["1.0.6"] = 4
        self.defaultTarget = "1.0.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def install(self):
        ret = CMakePackageBase.install(self)

        # Install bunzip2 symlink to bzip2, the behavior is altered in bzip2.c code by checking the program name.
        # See https://gitlab.com/bzip2/bzip2/-/blob/master/CMakeLists.txt?ref_type=heads#L378
        # We do it here be cause it is easier than to hack our CMake patch further.
        # CMake support has been added upstream and hopefully we can drop it all together ones version 1.1 is out
        linkSource = self.imageDir() / "bin" / f"bzip2{CraftCore.compiler.executableSuffix}"
        linkTarget = self.imageDir() / "bin" / f"bunzip2{CraftCore.compiler.executableSuffix}"
        utils.createShim(linkTarget, linkSource, keepArgv0=True)

        for file in glob.glob(os.path.join(self.imageDir(), "lib", "libbzip2.*")):
            utils.copyFile(file, os.path.join(self.imageDir(), "lib", "libbz2" + os.path.splitext(file)[1]), linkOnly=True)
        return ret
