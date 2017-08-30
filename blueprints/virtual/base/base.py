import info
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'

    def setDependencies(self):
        self.buildDependencies["gnuwin32/wget"] = "default"
        self.buildDependencies["dev-util/7zip"] = "default"
        self.buildDependencies["gnuwin32/patch"] = "default"
        self.buildDependencies["gnuwin32/sed"] = "default"
        self.buildDependencies["dev-util/cmake"] = "default"
        self.buildDependencies["dev-util/git"] = "default"

        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/mingw-w64"] = "default"
        if craftSettings.get("Compile", "MakeProgram", "") == "jom":
            self.buildDependencies["dev-util/jom"] = "default"
        if craftSettings.getboolean("Compile", "UseNinja", False):
            self.buildDependencies["dev-util/ninja"] = "default"
        if craftSettings.getboolean("Compile", "UseCCache", False):
            self.buildDependencies["dev-util/ccache"] = "default"

        self.runtimeDependencies["libs/runtime"] = "default"
        self.buildDependencies["craft/craft-blueprints-kde"] = "default"


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
