import glob
import os

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.Windows

    def setTargets(self):
        # not used  yet only for reference
        ver = str(CraftCore.compiler.getVersion())
        self.patchLevel[ver] = 2
        self.targets[ver] = ""
        self.description = "The compiler runtime package"
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        if CraftCore.compiler.compiler.isMinGW:
            self.buildDependencies["dev-utils/mingw-w64"] = None


class Package(BinaryPackageBase):
    def __init__(self, **args):
        super().__init__(**args)
        self.subinfo.options.package.disableBinaryCache = CraftCore.compiler.compiler.isMSVC

    def fetch(self):
        return True

    def unpack(self):
        return True

    def install(self):
        destdir = self.installDir() / "bin"
        utils.createDir(destdir)

        files = []
        if CraftCore.compiler.compiler.isMinGW:
            files = [
                "libgomp-1.dll",
                "libstdc++-6.dll",
                "libwinpthread-1.dll",
                "libgcc_s_seh-1.dll",
            ]
            srcdir = os.path.join(self.rootdir, "mingw64", "bin")
        elif CraftCore.compiler.compiler.isMSVC:
            redistDir = None
            if self.buildType() != "Debug":
                if CraftCore.compiler.getInternalVersion() >= 15:
                    if CraftCore.compiler.abi.isMSVC2022:
                        flavor = "2022"
                    elif CraftCore.compiler.abi.isMSVC2019:
                        flavor = "2019"
                    else:
                        raise Exception("Unknown compiler")
                    if "VCTOOLSREDISTDIR" in os.environ:
                        redistDir = os.environ["VCTOOLSREDISTDIR"]
                    else:
                        CraftCore.log.error(
                            f"Could not find Microsoft Visual Studio {flavor}.\n"
                            f"VCTOOLSREDISTDIR does not exist, and likely should point to '*\\Microsoft Visual Studio\\{flavor}\\Community\\VC\\Redist\\MSVC\\xx.xx.xxxxx'."
                        )
                if redistDir:
                    redistDir = os.path.join(redistDir, "x86" if CraftCore.compiler.architecture.isX86_32 else "x64")
                    files = glob.glob(
                        os.path.join(redistDir, "**/*.dll"),
                        recursive=True,
                    )
                    if not files:
                        CraftCore.log.error(f"No runtime files found in {redistDir}")
                        return False
                else:
                    CraftCore.log.error("Unsupported Compiler")
                    return False
        for f in files:
            if not os.path.isabs(f):
                f = os.path.join(srcdir, f)
            dest = os.path.join(destdir, os.path.basename(f))
            CraftCore.log.info(f"Installing: {dest}")
            if not utils.copyFile(f, dest, linkOnly=False):
                return False
        return True
