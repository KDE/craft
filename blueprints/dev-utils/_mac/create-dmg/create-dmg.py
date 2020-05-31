import info
from Package.MakeFilePackageBase import *

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.MacOS

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/andreyvit/create-dmg.git"
        self.targetInstallPath["master"] = "dev-utils/create-dmg"
        self.description = "A shell script to build fancy DMGs"
        self.webpage = "https://github.com/andreyvit/create-dmg"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        return True

    def postInstall(self):
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "create-dmg"),
                                os.path.join(self.imageDir(), "dev-utils", "create-dmg", "create-dmg"))
