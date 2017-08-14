import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['4.81'] = 'http://download.sysinternals.com/files/DebugView.zip'
        self.targetInstallPath['4.81'] = "dev-utils/bin"
        self.targetDigests['4.81'] = (
            ['98edbe8d5e10d8c81f91c1d79668df8dd3924abd6bb64e3450613c43bf0c60f6'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '4.81'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
