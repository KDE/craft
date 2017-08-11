import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.4.2", "2.5.5"]:
            self.targets[ver] = "http://downloads.sourceforge.net/winflexbison/win_flex_bison-%s.zip" % ver
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
        self.targetDigests['2.4.2'] = '9e6a3a0c2ca89c1afa068aa0a055c04f5e19b722'
        self.targetDigests['2.5.5'] = 'b86d22393f2e601523b60e529cecbd963628d4e8'
        self.defaultTarget = "2.5.5"

    def setDependencies(self):
        self.buildDependencies["gnuwin32/wget"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self): return False
        return \
            utils.copyFile(os.path.join(self.installDir(), "win_flex.exe"),
                           os.path.join(self.installDir(), "flex.exe")) and \
            utils.copyFile(os.path.join(self.installDir(), "win_bison.exe"),
                           os.path.join(self.installDir(), "bison.exe"))
