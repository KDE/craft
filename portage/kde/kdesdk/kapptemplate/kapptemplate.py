import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.shortDescription = "Factory for the easy creation of KDE/Qt components and programs"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['frameworks/kcoreaddons'] = 'default'
        self.runtimeDependencies['frameworks/kconfigwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kcompletion'] = 'default'
        self.runtimeDependencies['frameworks/karchive'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kdoctools'] = 'default'
        self.runtimeDependencies['dev-util/7zip'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
