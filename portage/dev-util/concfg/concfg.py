import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/lukesampson/concfg.git"
        self.targetInstallPath["master"] = "dev-utils/concfg/"

        self.description = "Concfg is a utility to import and export Windows console settings like fonts and colors."
        self.webpage = "https://github.com/lukesampson/concfg"

        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        return True

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "concfg.exe"),
                         utils.utilsCache.findApplication("powershell"),
                         args="-NoProfile {path}".format(
                             path=os.path.join(self.imageDir(), "dev-utils", "concfg", "bin", "concfg.ps1")),
                         useAbsolutePath=True)
        return True
