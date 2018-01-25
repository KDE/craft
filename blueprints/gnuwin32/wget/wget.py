import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["1.19.4"] = "http://downloads.sourceforge.net/sourceforge/tumagcc/wget-1.19.4_curl-7.58_aria2-1.33.1_dwnl.7z"
        self.targetInstallPath["1.19.4"] = "dev-utils"
        self.targetDigests['1.19.4'] = (['8f927eaba0011aca50b92327a24143b47278bdb724a662e999ddb171b84b2420'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.19.4"

    def setDependencies(self):
        self.buildDependencies["dev-util/7zip"] = "default"
        self.buildDependencies["core/cacert"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        utils.copyFile(os.path.join(self.sourceDir(), "wget.exe"),
                       os.path.join(self.installDir(), "bin", "wget.exe"))
        return True
