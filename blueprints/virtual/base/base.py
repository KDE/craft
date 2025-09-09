import info
from CraftCore import CraftCore
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.2"] = ""
        self.defaultTarget = "0.2"

    def setDependencies(self):
        # The order is important
        self.buildDependencies["core/cacert"] = None

        self.buildDependencies["dev-utils/7zip-base"] = None

        self.buildDependencies["dev-utils/mingw-w64"] = None
        self.buildDependencies["dev-utils/cmake-base"] = None
        self.buildDependencies["dev-utils/kshimgen"] = None
        self.buildDependencies["dev-utils/7zip"] = None
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["dev-utils/wget"] = None

        if CraftCore.compiler.platform.isLinux:
            self.buildDependencies["dev-utils/patchelf"] = None

        self.buildDependencies["dev-utils/git"] = None
        self.buildDependencies["dev-utils/patch"] = None
        self.buildDependencies["dev-utils/sed"] = None

        if CraftCore.compiler.platform.isWindows:
            self.buildDependencies["dev-utils/msys-base"] = None
        else:
            self.buildDependencies["dev-utils/automake"] = None
            self.buildDependencies["dev-utils/libtool"] = None

        if CraftCore.compiler.platform.isMacOS:
            self.buildDependencies["dev-utils/create-dmg"] = None

        if CraftCore.compiler.compiler.isMSVC or CraftCore.settings.get("Compile", "MakeProgram", "") == "jom":
            self.buildDependencies["dev-utils/jom"] = None
        if CraftCore.settings.getboolean("Compile", "UseNinja", False):
            self.buildDependencies["dev-utils/ninja"] = None

        self.runtimeDependencies["libs/runtime"] = None

        self.buildDependencies["libs/python"] = None

        # install the shim to the system python
        self.buildDependencies["dev-utils/system-python3"] = None

        if CraftCore.compiler.platform.isWindows:
            self.buildDependencies["dev-utils/msys"] = None

        # update the blueprints
        self.buildDependencies["craft/craft-blueprints-kde"] = None
        self.buildDependencies["craft/craft-core"] = None


class Package(VirtualPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
