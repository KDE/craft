import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "the next generation nepomuk"

    def setDependencies(self):
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['frameworks/kfilemetadata'] = 'default'
        self.runtimeDependencies['win32libs/lmdb'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
