import info
from Package.VirtualPackageBase import *


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

        if CraftCore.compiler.isLinux:
            self.buildDependencies["dev-utils/patchelf"] = None

        self.buildDependencies["dev-utils/git"] = None
        self.buildDependencies["python-modules/pip-system"] = None
        self.buildDependencies["python-modules/virtualenv"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.buildDependencies["dev-utils/python3"] = None

        self.buildDependencies["dev-utils/patch"] = None
        self.buildDependencies["dev-utils/sed"] = None
        self.buildDependencies["dev-utils/automake"] = None
        self.buildDependencies["dev-utils/libtool"] = None

        if CraftCore.compiler.isMacOS:
            self.buildDependencies["dev-utils/create-dmg"] = None

        if CraftCore.compiler.isMSVC() or CraftCore.settings.get("Compile", "MakeProgram", "") == "jom":
            self.buildDependencies["dev-utils/jom"] = None
        if CraftCore.settings.getboolean("Compile", "UseNinja", False):
            self.buildDependencies["dev-utils/ninja"] = None

        self.buildDependencies["craft/craft-blueprints-kde"] = None
        self.buildDependencies["craft/craft-core"] = None
        self.runtimeDependencies["libs/runtime"] = None


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
