import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        # The master target will (currently) build Kirigami's 2.x work.
        # We need the release version, at least until 2.x has had an
        # official release, and as such we set the detault to 1.1
        for ver in ["1.0.0", "1.0.1", "1.0.2", "1.1.0"]:
            self.targets[ver] = "http://download.kde.org/stable/kirigami/kirigami-" + ver + ".tar.xz"
            self.targetInstSrc[ ver ] = 'kirigami-' + ver
        self.defaultTarget = "1.1.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["libs/qtgraphicaleffects"] = "default"
        self.runtimeDependencies["libs/qtquickcontrols2"] = "default"

from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DDESKTOP_ENABLED=ON '
