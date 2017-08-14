import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['16.21'] = 'http://download.sysinternals.com/files/ProcessExplorer.zip'
        self.defaultTarget = '16.21'
        self.targetDigests['16.21'] = (
            ['9f32608a5f9ce2d2eb0fe9cdfe65ebc06f7c3c2b52d2b6b1bf3737af9a2d2bad'], CraftHash.HashAlgorithm.SHA256)
        # the zip file does not have a bin dir, so we have to create it
        # This attribute is in prelimary state
        self.targetInstallPath['16.21'] = os.path.join("dev-util", "bin")


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
