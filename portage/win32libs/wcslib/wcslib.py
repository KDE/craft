import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.1'] = 'http://indilib.org/jdownloads/kstars/wcslib-515.tar.bz2'

        self.defaultTarget = '0.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DENABLE_STATIC=ON"
