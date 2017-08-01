import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['libs/qtactiveqt'] = 'default'
        self.runtimeDependencies['libs/qtdeclarative'] = 'default'
        self.runtimeDependencies['libs/qtgraphicaleffects'] = 'default'
        self.runtimeDependencies['libs/qtimageformats'] = 'default'
        self.runtimeDependencies['libs/qtmultimedia'] = 'default'
        self.runtimeDependencies['libs/qtscript'] = 'default'
        self.runtimeDependencies['libs/qtsvg'] = 'default'
        self.runtimeDependencies['libs/qttools'] = 'default'
        self.runtimeDependencies['libs/qtwebkit'] = 'default'
        self.runtimeDependencies['libs/qtwebchannel'] = 'default'
        self.runtimeDependencies['libs/qtxmlpatterns'] = 'default'
        self.runtimeDependencies['libs/qtwinextras'] = 'default'
        self.runtimeDependencies['libs/qtquickcontrols'] = 'default'
        self.runtimeDependencies['libs/qtquickcontrols2'] = 'default'
        self.runtimeDependencies['libs/qtserialport'] = 'default'


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
