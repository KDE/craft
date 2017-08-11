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


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--enable-sdk=all --enable-secure-api --without-crt"
