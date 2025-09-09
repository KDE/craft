import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = ~CraftCore.compiler.Platforms.Android

    def setTargets(self):
        for ver in ["2.16.03"]:
            if CraftCore.compiler.compiler.isMSVC:
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/nasm/{ver}/nasm-{ver}-win64.zip"
                self.targetDigestUrls[ver] = f"https://files.kde.org/craft/3rdparty/nasm/{ver}/nasm-{ver}-win64.zip.sha256"
            else:
                self.targets[ver] = f"https://files.kde.org/craft/3rdparty/nasm/{ver}/nasm-{ver}.tar.xz"
                self.targetDigestUrls[ver] = f"https://files.kde.org/craft/3rdparty/nasm/{ver}/nasm-{ver}.tar.xz.sha256"

            self.targetInstSrc[ver] = f"nasm-{ver}"
            if CraftCore.compiler.compiler.isMSVC:
                self.targetInstallPath[ver] = "dev-utils/bin"
            else:
                self.targetInstallPath[ver] = "dev-utils"
        self.description = "This is NASM - the famous Netwide Assembler"
        self.webpage = "https://www.nasm.us/"
        self.defaultTarget = "2.16.03"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.compiler.isMSVC:

    class Package(BinaryPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.useShadowBuild = not CraftCore.compiler.platform.isWindows
            self.subinfo.options.configure.autoreconf = False
