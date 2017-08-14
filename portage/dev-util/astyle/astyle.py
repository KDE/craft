import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["2.0.4"] = "http://downloads.sourceforge.net/sourceforge/astyle/AStyle_2.04_windows.zip"
        self.targetInstSrc["2.0.4"] = "AStyle"
        self.targetInstallPath["2.0.4"] = "dev-utils"
        self.targetDigests['2.0.4'] = (
            ['55af23dc101154f9645c10e3352142b6e8bc4992ec82953677f6a03f4a7e10be'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '2.0.4'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
