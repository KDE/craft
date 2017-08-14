import info

from Package.MSBuildPackageBase import MSBuildPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.2.1"]:
            self.targets[ver] = "https://github.com/winlibs/libffi/archive/libffi-%s.tar.gz" % ver
            self.archiveNames[ver] = "libffi-libffi-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libffi-libffi-%s" % ver
        self.targetDigests['3.2.1'] = (
            ['9f8e1133c6b9f72b73943103414707a1970e2e9b1d332c3df0d35dac1d9917e5'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.2.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


class PackageCMake(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)

        self.arch = "x86"
        if craftCompiler.isX64():
            self.arch = "x64"
        self.subinfo.options.configure.projectFile = os.path.join(self.sourceDir(), "win32", f"vc14_{self.arch}",
                                                                  "libffi-msvc.sln")

    def install(self):
        if not MSBuildPackageBase.install(self, installHeaders=False):
            return False
        utils.copyFile(os.path.join(self.sourceDir(), "include", "ffi.h"),
                       os.path.join(self.imageDir(), "include", "ffi.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "include", "ffi_common.h"),
                       os.path.join(self.imageDir(), "include", "ffi_common.h"), False)
        return True


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--enable-shared --disable-static "


if craftCompiler.isMinGW():
    class Package(PackageMSys):
        pass
else:
    class Package(PackageCMake):
        pass
