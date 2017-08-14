import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.8.17"]:
            self.targets[ver] = f"http://downloads.sourceforge.net/win32svn/{ver}/apache22/svn-win32-{ver}.zip"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "svn")
            self.targetInstSrc[ver] = f"svn-win32-{ver}"
        self.targetDigests['1.8.17'] = (
            ['1d919a21bd8ad39ff250702c3d51796b525932845bd27a09a1f7dd144dff9245'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.8.17"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        utils.copyFile(os.path.join(self.packageDir(), "svn.bat"),
                       os.path.join(self.rootdir, "dev-utils", "bin", "svn.bat"))
        return True
