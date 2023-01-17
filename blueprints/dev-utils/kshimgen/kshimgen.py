import info
from Package.CMakePackageBase import *
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/sdk/kshim.git"

        for ver in ["0.5.4"]:
            if CraftCore.compiler.isAndroid:
                # we need kshimgen only as a host tool, on Android we need to use a pre-build binary, since it doesn't build on Android natively
                self.targets[ver] = f"https://download.kde.org/stable/kshimgen/{ver}/kshimgen-{ver}-linux-binary.tar.gz"
                self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kshimgen/{ver}/kshimgen-{ver}-linux-binary.tar.gz.sha256"
                self.targetInstallPath[ver] = "dev-utils/bin"
            else:
                # on all other platforms we build kshimgen from source
                self.targets[ver] = f"https://invent.kde.org/sdk/kshim/-/archive/v{ver}/kshim-v{ver}.tar.gz"
                self.targetInstSrc[ver] = f"kshim-v{ver}"


        if not CraftCore.compiler.isAndroid:
            self.targetDigests["0.5.4"] = (
                ["f0df8b089c8464335c9599c73b83704798ff1adbe18707e7e91fc058345dbb4e"],
                CraftHash.HashAlgorithm.SHA256,
            )

        self.defaultTarget = "0.5.4"

    if not CraftCore.compiler.isAndroid:
        def setDependencies(self):
            self.buildDependencies["dev-utils/cmake-base"] = None
            self.buildDependencies["dev-utils/mingw-w64"] = None


if CraftCore.compiler.isAndroid:
    class Package(BinaryPackageBase):
        def __init__(self):
            BinaryPackageBase.__init__(self)

        def install(self):
            return utils.copyDir(self.sourceDir(), self.installDir())

else:
    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)

        def configure(self):
            cmakePath = Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/cmake-base"
            if OsUtils.isMac():
                cmakePath /= "CMake.app/Contents/bin"
            else:
                cmakePath /= "bin"
            path = f"{cmakePath}{os.pathsep}{os.environ['PATH']}"
            with utils.ScopedEnv({"PATH": path}):
                return super().configure()
