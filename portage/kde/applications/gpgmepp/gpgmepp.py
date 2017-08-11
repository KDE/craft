import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "GpgME++ is a C++ wrapper (or C++ bindings) for the GnuPG project's gpgme (GnuPG Made Easy) library, version 0.4.4 and later."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["win32libs/gpgme"] = "default"
        self.runtimeDependencies["win32libs/boost/boost-headers"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
