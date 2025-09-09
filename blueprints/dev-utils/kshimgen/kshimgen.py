import os

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/sdk/kshim.git"
        self.svnTargets["append"] = "https://invent.kde.org/sdk/kshim.git|work/append|"

        for ver in ["0.6.1"]:
            if CraftCore.compiler.platform.isAndroid:
                # we need kshimgen only as a host tool, on Android we need to use a pre-build binary, since it doesn't build on Android natively
                self.targets[ver] = f"https://download.kde.org/stable/kshim/kshim-v{ver}-linux-binary-x86_64.tar.7z"
                self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kshim/kshim-v{ver}-linux-binary-x86_64.tar.7z.sha256"
                self.targetInstallPath[ver] = "dev-utils"
            else:
                # on all other platforms we build kshimgen from source
                self.targets[ver] = f"https://download.kde.org/stable/kshim/kshim-{ver}.tar.xz"
                self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kshim/kshim-{ver}.tar.xz.sha256"
                self.targetInstSrc[ver] = f"kshim-{ver}"
        self.defaultTarget = "0.6.1"

    if not CraftCore.compiler.platform.isAndroid:

        def setDependencies(self):
            self.buildDependencies["dev-utils/cmake-base"] = None
            self.buildDependencies["dev-utils/mingw-w64"] = None


if CraftCore.compiler.platform.isAndroid:

    class Package(BinaryPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def install(self):
            return utils.copyDir(self.sourceDir(), self.installDir())

else:

    class Package(CMakePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if CraftCore.compiler.platform.isMacOS:
                self.subinfo.options.configure.args += ["-DCMAKE_OSX_ARCHITECTURES=arm64;x86_64"]

        def configure(self):
            cmakePath = CraftCore.standardDirs.craftRoot() / "dev-utils/cmake-base"
            if CraftCore.compiler.platform.isMacOS:
                cmakePath /= "CMake.app/Contents/bin"
            else:
                cmakePath /= "bin"
            path = f"{cmakePath}{os.pathsep}{os.environ['PATH']}"
            with utils.ScopedEnv({"PATH": path}):
                return super().configure()
