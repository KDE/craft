import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.19.2"]:
            self.targets[ver] = f"https://eternallybored.org/misc/wget/releases/wget-{ver}-win{CraftCore.compiler.bits}.zip"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targetDigests["1.19.2"] = (['2350a4391c6c3b666b6aaf11842009869fba1deae1dfbf4c005e2dc135c69148'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigestsX64["1.19.2"] = (['34d76a8a75315ccacf9fdd6f0d928b663f74d8ff641de3bbc822f704b82e57ad'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.19.2"

    def setDependencies(self):
        self.buildDependencies["dev-util/7zip"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

