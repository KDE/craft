import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.8.7', '1.8.9.1', '1.8.11']:
            self.targets[ver] = 'ftp://ftp.stack.nl/pub/users/dimitri/doxygen-%s.windows.bin.zip' % ver
            self.targetInstallPath[ver] = "dev-utils/bin"

        self.targetDigests['1.8.7'] = 'ca9640fbb28695f16521e5eacf49f278ff192d1c'
        self.targetDigests['1.8.9.1'] = '942a40755c537ad31cc18c8e519377db66edff29'
        self.targetDigests['1.8.11'] = (
            ['f25964e0203739d77e79d74bafdbef212bd97748e20fdafad078a8e2d315a7ff'], CraftHash.HashAlgorithm.SHA256)

        self.description = 'Automated C, C++, and Java Documentation Generator'
        self.defaultTarget = '1.8.11'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
