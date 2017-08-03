import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtactiveqt"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtgraphicaleffects"] = "default"
        self.runtimeDependencies["libs/qt5/qtimageformats"] = "default"
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = "default"
        self.runtimeDependencies["libs/qt5/qtscript"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt5/qttools"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebchannel"] = "default"
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = "default"
        self.runtimeDependencies["libs/qt5/qtwinextras"] = "default"
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = "default"
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = "default"
        self.runtimeDependencies["libs/qt5/qtserialport"] = "default"


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
