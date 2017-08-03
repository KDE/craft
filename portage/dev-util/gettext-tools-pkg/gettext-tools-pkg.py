import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.18.1.1'] = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-0.18.1.1.tar.gz'
        self.targetDigests['0.18.1.1'] = '5009deb02f67fc3c59c8ce6b82408d1d35d4e38f'
        self.targetInstSrc['0.18.1.1'] = 'gettext-0.18.1.1'
        self.defaultTarget = '0.18.1.1'

    def setDependencies(self):
        self.runtimeDependencies["dev-util/perl"] = "default"
        self.runtimeDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["win32libs/win_iconv"] = "default"


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--disable-java --disable-csharp --disable-shared --enable-static --with-gettext-tools "
