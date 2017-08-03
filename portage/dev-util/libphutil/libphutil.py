import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/phacility/libphutil.git"
        self.targetInstallPath["master"] = "dev-utils/arcanist/libphutil"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"
        self.buildDependencies["binary/php"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        return True
