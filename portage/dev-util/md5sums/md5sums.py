import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['20080511'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/md5sums-20080511-bin.zip"
        self.targetInstallPath["20080511"] = "dev-utils"
        self.defaultTarget = '20080511'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
