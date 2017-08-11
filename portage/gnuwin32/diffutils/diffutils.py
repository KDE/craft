import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['2.8.7-1'] = ["http://downloads.sourceforge.net/sourceforge/gnuwin32/diffutils-2.8.7-1-bin.zip",
                                   "http://downloads.sourceforge.net/sourceforge/gnuwin32/diffutils-2.8.7-1-dep.zip"]
        self.targetInstallPath["2.8.7-1"] = "dev-utils"
        self.targetDigests['2.8.7-1'] = ['892460fee6f19ff38d70872ac565fbb97f9d3c16',
                                         '426636df15901f95b0f2a57ef325e876695aaa57']
        self.defaultTarget = '2.8.7-1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
