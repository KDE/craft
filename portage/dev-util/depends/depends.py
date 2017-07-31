import info


class subinfo(info.infoclass):
    def setTargets(self):
        arch = "x86"
        if craftCompiler.isX64():
            arch = "x64"
        self.targets['2.2'] = 'http://www.dependencywalker.com/depends22_' + arch + '.zip'
        self.targetInstallPath['2.2'] = "dev-utils/bin"
        self.defaultTarget = '2.2'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
