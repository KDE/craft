import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.7.2']:
            self.targets[ver] = 'http://www.mpir.org/mpir-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = "mpir-" + ver
        self.targetDigests['2.7.2'] = 'a285352d4299eb18d4f02a97e3232efab225e174'
        self.targetInstSrc['2.7.2'] = 'mpir-2.7.2'

        self.description = "Library for arbitrary precision integer arithmetic derived from version 4.2.1 of gmp"
        self.defaultTarget = '2.7.2'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"
        else:
            self.buildDependencies["dev-util/yasm"] = "default"


from Package.AutoToolsPackageBase import *
from Package.MSBuildPackageBase import *


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        abi = "ABI=64"
        if craftCompiler.isX86():
            abi = "ABI=32"
            self.platform = ""
        self.subinfo.options.configure.args = "--enable-shared --disable-static --enable-gmpcompat --enable-cxx " + abi


class PackageMSVC(MSBuildPackageBase):
    def __init__(self, **args):
        MSBuildPackageBase.__init__(self)
        self.mpirBuildDir = os.path.join(self.sourceDir(), "build.vc14")
        self.subinfo.options.configure.projectFile = os.path.join(self.mpirBuildDir, "mpir.sln")
        self.msbuildTargets = ["dll_mpir_gc", "lib_mpir_cxx"]

    def make(self):
        utils.putenv('YASMPATH', os.path.join(self.rootdir, 'dev-utils', 'bin'))
        return MSBuildPackageBase.make(self)

    def install(self):
        if not MSBuildPackageBase.install(self, buildDirs=[os.path.join(self.mpirBuildDir, target) for target in
                                                           self.msbuildTargets]):
            return False
        # a dirty workaround the fact that FindGMP.cmake will only look for gmp.lib
        utils.copyFile(os.path.join(self.installDir(), "lib", "mpir.lib"),
                       os.path.join(self.installDir(), "lib", "gmp.lib"))
        return True


if craftCompiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(PackageMSVC):
        def __init__(self):
            PackageMSVC.__init__(self)
