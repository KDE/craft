import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

    def setTargets(self):
        for ver in ['3.0', '4.1']:
            self.targets[ver] = 'http://download.gna.org/getfem/stable/gmm-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'gmm-' + ver
        self.defaultTarget = '4.1'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        src = os.path.join(self.packageDir(), "CMakeLists.txt")
        dst = os.path.join(self.sourceDir(), "CMakeLists.txt")
        utils.copyFile(src, dst)
        return True
