import info
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'

    def setDependencies(self):
        self.buildDependencies["dev-utils/wget"] = "default"
        self.buildDependencies["dev-utils/7zip"] = "default"
        self.buildDependencies["dev-utils/patch"] = "default"
        self.buildDependencies["dev-utils/sed"] = "default"
        self.buildDependencies["dev-utils/cmake"] = "default"
        self.buildDependencies["dev-utils/git"] = "default"

        if CraftCore.compiler.isMacOS:
            self.buildDependencies["dev-util/macdylibbundler"] = "default"


        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/mingw-w64"] = "default"
        if CraftCore.settings.get("Compile", "MakeProgram", "") == "jom":
            self.buildDependencies["dev-utils/jom"] = "default"
        if CraftCore.settings.getboolean("Compile", "UseNinja", False):
            self.buildDependencies["dev-utils/ninja"] = "default"
        if CraftCore.settings.getboolean("Compile", "UseCCache", False):
            self.buildDependencies["dev-utils/ccache"] = "default"

        self.runtimeDependencies["libs/runtime"] = "default"
        self.buildDependencies["craft/craft-blueprints-kde"] = "default"
        self.buildDependencies["craft/craft-core"] = "default"

        # needed by CollectionPackagerBase
        if (CraftCore.settings.getboolean("QtSDK", "Enabled", False) and
            CraftCore.settings.getboolean("QtSDK","PackageQtSDK",True)):
            self.buildDependencies["dev-utils/dependencies"] = "default"


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
