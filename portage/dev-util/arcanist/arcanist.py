import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/phacility/arcanist.git"
        self.targetInstallPath["master"] = "dev-utils/arcanist/arcanist"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"
        self.buildDependencies["binary/php"] = "default"
        self.buildDependencies["dev-util/libphutil"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        return True

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "arc.exe"),
                         os.path.join(
                             os.path.join(self.imageDir(), "dev-utils", "arcanist", "arcanist", "bin", "arc.bat")))
        return True
