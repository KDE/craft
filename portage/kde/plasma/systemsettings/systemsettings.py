import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kguiaddons'] = 'default'
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = 'default'
        self.runtimeDependencies['frameworks/kservice'] = 'default'
        self.runtimeDependencies['frameworks/kcompletion'] = 'default'
        self.runtimeDependencies['frameworks/frameworkintegration'] = 'default'
        self.runtimeDependencies['frameworks/kwindowsystem'] = 'default'
        self.runtimeDependencies['frameworks/kcmutils'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
