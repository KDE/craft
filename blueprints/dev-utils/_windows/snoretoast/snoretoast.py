import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.5.2"]:
            self.targets[ver] = "https://download.kde.org/stable/snoretoast/0.5.2/bin/snoretoast_v0.5.2-x64.7z"
            self.targetInstSrc[ver] = "snoretoast_v0.5.2-x64"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["0.5.2"] = (["94209bbf777265bfbd5b77fde4e0ff5801509db043e0575ee00ba5736d2e946f"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A command line application capable of creating Windows Toast notifications."
        self.webpage = "https://phabricator.kde.org/source/snoretoast/"
        self.displayName = "SnoreToast"
        self.defaultTarget = "0.5.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
