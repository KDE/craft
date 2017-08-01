import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.shortDescription = "Graphical File Differences Tool"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['kde/libkomparediff2'] = 'default'
        self.runtimeDependencies['frameworks/kcoreaddons'] = 'default'
        self.runtimeDependencies['frameworks/kcodecs'] = 'default'
        self.runtimeDependencies['frameworks/kdoctools'] = 'default'
        self.runtimeDependencies['frameworks/kiconthemes'] = 'default'
        self.runtimeDependencies['frameworks/kjobwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kparts'] = 'default'
        self.runtimeDependencies['frameworks/ktexteditor'] = 'default'
        self.runtimeDependencies['frameworks/kwidgetsaddons'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
