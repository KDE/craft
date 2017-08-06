import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"

    def setTargets(self):
        for ver in ["3.0"]:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/nsis/nsis-3.0.zip"
            self.targetInstSrc[ver] = "nsis-%s" % ver
            self.targetInstallPath[ver] = os.path.join("dev-utils", "nsis")

        self.targetDigests['3.0'] = '58817baa6509ad239f6cdff90ac013689aff1902'
        self.defaultTarget = '3.0'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        for name in ['makensis', 'makensisw', 'nsis']:
            if not utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", f"{name}.exe"),
                                    os.path.join(self.imageDir(), "dev-utils", "nsis", f"{name}.exe")):
                return False
        return True
