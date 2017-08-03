import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver, rev, rt in [("5.3.0", "0", "4"), ("5.4.0", "0", "5"), ("6.2.0", "0", "5"), ("7.1.0", "0", "5")]:
            arch = "i686" if craftCompiler.isX86() else "x86_64"
            exceptionType = "sjlj" if craftCompiler.isX86() else "seh"
            self.targets[
                f"{ver}-{rev}"] = f"http://downloads.sourceforge.net/sourceforge/mingw-w64/{arch}-{ver}-release-posix-{exceptionType}-rt_v{rt}-rev{rev}.7z"

        self.defaultTarget = "7.1.0-0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class PackageMinGW(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if craftCompiler.isX86():
            return utils.moveDir(os.path.join(self.installDir(), "mingw32"), os.path.join(self.installDir(), "mingw"))
        return True


from Package.Qt5CorePackageBase import *


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, condition=craftCompiler.isMinGW(), classA=PackageMinGW)
