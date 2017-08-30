import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets[
            "1.18"] = "http://downloads.sourceforge.net/sourceforge/tumagcc/wget-1.18_curl-7.49.1_win32_win64.7z"
        self.targetInstallPath["1.18"] = "dev-utils"
        self.targetDigests['1.18'] = (
            ['19d4ae30ae35f212e95edb6f18dddab19e1c97e119c36c4231b741e7293f9b3c'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.18"

    def setDependencies(self):
        self.buildDependencies["dev-util/7zip"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if craftCompiler.isX64():
            utils.copyFile(os.path.join(self.sourceDir(), "wget64.exe"),
                           os.path.join(self.installDir(), "bin", "wget.exe"))
        else:
            utils.copyFile(os.path.join(self.sourceDir(), "wget.exe"),
                           os.path.join(self.installDir(), "bin", "wget.exe"))
        utils.copyFile(os.path.join(self.sourceDir(), "curl-ca-bundle.crt"),
                       os.path.join(self.installDir(), "bin", "curl-ca-bundle.crt"))
        return True
