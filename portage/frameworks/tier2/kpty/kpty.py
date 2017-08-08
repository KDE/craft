import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Pty abstraction"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"


from Package.CMakePackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class UnixPackage(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)


if OsUtils.isUnix():
    class Package(UnixPackage):
        def __init__(self):
            UnixPackage.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
