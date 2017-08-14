import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        # qtquick1 is optional
        # self.runtimeDependencies['libs/qtquick1'] = 'default'

    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:phonon'
        for ver in ['4.9.0', '4.9.1']:
            self.targets[ver] = 'http://download.kde.org/stable/phonon/%s/phonon-%s.tar.xz' % (ver, ver)
            self.targetInstSrc[ver] = 'phonon-%s' % ver
        self.targetDigests['4.9.0'] = (
            ['bb74b40f18ade1d9ab89ffcd7aeb7555be797ca395f1224c488b394da6deb0e0'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['4.9.1'] = (
            ['67bee986f85ca8b575186c8ba58a85886cb3b1c3567c86a118d56129f221e69c'], CraftHash.HashAlgorithm.SHA256)

        self.description = "a Qt based multimedia framework"
        self.defaultTarget = '4.9.1'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DPHONON_BUILD_EXAMPLES=OFF -DPHONON_BUILD_TESTS=OFF -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT=ON -DPHONON_BUILD_PHONON4QT5=ON"
        if not self.subinfo.options.isActive("win32libs/dbus"):
            self.subinfo.options.configure.args += " -DPHONON_NO_DBUS=ON "
