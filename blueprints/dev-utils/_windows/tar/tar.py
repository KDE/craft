import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedBuild("https://files.kde.org/craft/prebuilt/packages/", packagePath="prebuilt/binary/tar")

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = None

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

