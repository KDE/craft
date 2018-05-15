import info


class subinfo(info.infoclass):
    def setTargets(self):
        fileNames = {"1.19.4":"wget-1.19.4_curl-7.58_aria2-1.33.1_dwnl.7z",
                  "1.19.2":"wget-1.19.2_curl-7.56.1_aria2-1.33_dwnl_rev2.7z",
                  "1.18":"wget-1.18_curl-7.49.1_win32_win64.7z"}
        for ver in ["1.18", "1.19.2", "1.19.4"]:
            fName = fileNames[ver]
            self.targets[ver] = f"http://downloads.sourceforge.net/sourceforge/tumagcc/{fName}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests['1.18'] = (['19d4ae30ae35f212e95edb6f18dddab19e1c97e119c36c4231b741e7293f9b3c'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.19.2'] = (['0791cce5bf665edcc295cbdc58c4b30568f052a485f88672691abf92a7e80dac'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.19.4'] = (['8f927eaba0011aca50b92327a24143b47278bdb724a662e999ddb171b84b2420'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.18"

    def setDependencies(self):
        self.buildDependencies["dev-utils/7zip"] = "default"
        self.buildDependencies["core/cacert"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        utils.copyFile(os.path.join(self.sourceDir(), "wget.exe"),
                       os.path.join(self.installDir(), "bin", "wget.exe"))
        return True

    def postQmerge(self):
        CraftCore.cache.clear()
