import info


class subinfo(info.infoclass):
    def setTargets(self):
        # not used  yet only for reference
        self.targets['master'] = ""
        self.description = "the mingw compiler runtime package"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        if craftCompiler.isMinGW():
            self.buildDependencies["dev-util/mingw-w64"] = "default"


from Package.BinaryPackageBase import *


class PackageMinGW(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.version = craftCompiler.getVersion()

    def fetch(self):
        return True

    def unpack(self):
        destdir = os.path.join(self.sourceDir(), "bin")
        utils.createDir(self.sourceDir())
        utils.createDir(destdir)

        if not OsUtils.isWin():
            return True

        files = ['libgomp-1.dll', 'libstdc++-6.dll', 'libwinpthread-1.dll']
        if craftCompiler.isMinGW_W32():
            files.append('libgcc_s_sjlj-1.dll')
            srcdir = os.path.join(self.rootdir, "mingw", "bin")
        elif craftCompiler.isMinGW_W64():
            files.append('libgcc_s_seh-1.dll')
            srcdir = os.path.join(self.rootdir, "mingw64", "bin")

        for file in files:
            utils.copyFile(os.path.join(srcdir, file), os.path.join(destdir, file), linkOnly=False)
        return True


from Package.Qt5CorePackageBase import *


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, condition=craftCompiler.isMinGW(), classA=PackageMinGW)
