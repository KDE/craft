import info


# see http://eigen.tuxfamily.org/ for more informations

class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

    def setTargets(self):
        for ver in ['2.0.17']:
            self.targets[ver] = 'http://bitbucket.org/eigen/eigen/get/2.0.17.tar.bz2'
            self.targetInstSrc[ver] = 'eigen-eigen-b23437e61a07'
        self.targetDigests['2.0.17'] = '461546be98b964d8d5d2adb0f1c31ba0e42efc38'
        self.defaultTarget = '2.0.17'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_TESTS=OFF"
        # header-only package
        self.subinfo.options.package.withCompiler = False
