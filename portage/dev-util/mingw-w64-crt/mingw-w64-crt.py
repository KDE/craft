import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://git.code.sf.net/p/mingw-w64/mingw-w64'

        if craftCompiler.isX64():
            self.targetInstallPath["master"] = "mingw64/x86_64-w64-mingw32"
        else:
            self.targetInstallPath["master"] = "mingw/i686-w64-mingw32"

        self.defaultTarget = 'master'

    def setDependencies(self):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["dev-util/mingw-w64-headers"] = "default"


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.supportsCCACHE = False
        if craftCompiler.isX64():
            disable = "--disable-lib32 --enable-lib64"
        else:
            disable = "--disable-lib64 --enable-lib32"
        self.subinfo.options.configure.args = " --with-sysroot=%s --enable-wildcard --without-headers  %s  " % (
        self.shell.toNativePath(self.mergeDestinationDir()), disable)
