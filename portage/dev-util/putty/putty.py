import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.70"]:
            self.targets[ver] = f"https://the.earth.li/~sgtatham/putty/{ver}/w{craftCompiler.bits}/putty.zip"
            self.archiveNames[ver] = f"putty-{ver}.zip"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")

            self.targetDigestsX64['0.70'] = (['8422ad5fe060b7229fbf51512e3eb23c5bfe631eb660e9604343e5e81b69fad0'], CraftHash.HashAlgorithm.SHA256)
            self.targetDigests['0.70'] = (['8422ad5fe060b7229fbf51512e3eb23c5bfe631eb660e9604343e5e81b69fad0'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.70"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
