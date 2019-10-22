import info
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'

    def setDependencies(self):
        # The order is important
        self.buildDependencies["core/cacert"] = None
        if CraftCore.compiler.isWindows:
            self.buildDependencies["dev-utils/7zip"] = None
            self.buildDependencies["dev-utils/wget"] = None
            self.buildDependencies["dev-utils/git"] = None
            self.buildDependencies["dev-utils/kshimgen"] = None
            self.buildDependencies["dev-utils/cmake"] = None
        else:
            self.buildDependencies["dev-utils/cmake"] = None
            self.buildDependencies["dev-utils/7zip"] = None

        self.buildDependencies["python-modules/virtualenv"] = None
        self.buildDependencies["dev-utils/python3"] = None

        self.buildDependencies["dev-utils/patch"] = None
        self.buildDependencies["dev-utils/sed"] = None
        self.buildDependencies["dev-utils/automake"] = None
        self.buildDependencies["dev-utils/libtool"] = None

        if CraftCore.compiler.isMacOS:
            self.buildDependencies["dev-utils/create-dmg"] = None


        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/mingw-w64"] = None
        if CraftCore.settings.get("Compile", "MakeProgram", "") == "jom":
            self.buildDependencies["dev-utils/jom"] = None
        if CraftCore.settings.getboolean("Compile", "UseNinja", False):
            self.buildDependencies["dev-utils/ninja"] = None
        if CraftCore.settings.getboolean("Compile", "UseCCache", False):
            self.buildDependencies["dev-utils/ccache"] = None

        # needed by CollectionPackagerBase
        if (CraftCore.settings.getboolean("QtSDK", "Enabled", False) and
                CraftCore.settings.getboolean("QtSDK","PackageQtSDK",True)):
            self.buildDependencies["dev-utils/dependencies"] = None

        self.buildDependencies["craft/craft-blueprints-kde"] = None
        self.buildDependencies["craft/craft-core"] = None
        self.runtimeDependencies["libs/runtime"] = None
        if CraftCore.settings.getboolean("General", "AllowAnsiColor", False):
            self.buildDependencies["python-modules/coloredlogs"] = None



class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
