import info
import glob

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Windows

    def setTargets(self):
        # not used  yet only for reference
        ver = str(CraftCore.compiler.getVersion())
        self.patchLevel[ver] = 2
        self.targets[ver] = ""
        self.description = "The compiler runtime package"
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/mingw-w64"] = None


from Package.BinaryPackageBase import *


class PackageWin(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = CraftCore.compiler.isMSVC()

    def fetch(self):
        return True

    def unpack(self):
        return True

    def install(self):
        destdir = os.path.join(self.installDir(), "bin")
        utils.createDir(destdir)

        files = []
        if CraftCore.compiler.isMinGW():
            files = ['libgomp-1.dll', 'libstdc++-6.dll', 'libwinpthread-1.dll', 'libgcc_s_seh-1.dll', 'libssp-0.dll']
            srcdir = os.path.join(self.rootdir, "mingw64", "bin")
        elif CraftCore.compiler.isMSVC():
            redistDir = None
            if self.buildType() != "Debug":
                if CraftCore.compiler.getInternalVersion() >= 15:
                    if CraftCore.compiler.isMSVC2022():
                        flavor="2022"
                    elif CraftCore.compiler.isMSVC2019():
                        flavor="2019"
                    elif CraftCore.compiler.isMSVC2017():
                        flavor="2017"
                    else:
                        raise Exception("Unknown compiler")
                    if "VCTOOLSREDISTDIR" in os.environ:
                        redistDir = os.environ["VCTOOLSREDISTDIR"]
                    else:
                        CraftCore.log.error(f"Could not find Microsoft Visual Studio {flavor}.\n"
                                            f"VCTOOLSREDISTDIR does not exist, and likely should point to '*\\Microsoft Visual Studio\\{flavor}\\Community\\VC\\Redist\\MSVC\\xx.xx.xxxxx'.")
                elif CraftCore.compiler.isMSVC2015():
                    if "VCINSTALLDIR" in os.environ:
                        redistDir = os.path.join(os.environ["VCINSTALLDIR"], "redist")
                    else:
                        CraftCore.log.error("Could not find Microsoft Visual Studio 2015.\n" +
                                            r"VCINSTALLDIR does not exist, and should point to '*\Microsoft Visual Studio\2015\Community\VC\'.")
                if redistDir:
                    files = glob.glob(os.path.join(redistDir, CraftCore.compiler.architecture, "**/*.dll"), recursive=True)
                else:
                    CraftCore.log.error("Unsupported Compiler")
                    return False
        for f in files:
            if not os.path.isabs(f):
                f = os.path.join(srcdir, f)
            utils.copyFile(f, os.path.join(destdir, os.path.basename(f)), linkOnly=False)
        return True


from Package.Qt5CorePackageBase import *


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, condition=OsUtils.isWin(), classA=PackageWin)
