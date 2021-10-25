import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.9", "1.10", "1.11"]:
            self.targets[ver] = f"https://github.com/lucasg/Dependencies/releases/download/v{ver}/Dependencies_x64_Release.zip"
            self.archiveNames[ver] = f"dependencies-{ver}.zip"
            self.targetInstallPath[ver] = "dev-utils/dependencies/"

        self.targetDigests["1.9"] = (['dae97fb67329b61d3d2e2a37a583a14e89bb6e3c0f7fed62e5d8a03cffb6703f'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.11"] = (['820215f3107c135635ded01de2fb0785797cf1fe5fae1cedb6f0afc42f91881b'], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://github.com/lucasg/Dependencies"
        self.description = "A rewrite of the old legacy software \"depends.exe\" in C# for Windows devs to troubleshoot dll load dependencies issues."
        self.defaultTarget = "1.11"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "dependenciesgui.exe"),
                         os.path.join(self.imageDir(), "dev-utils", "dependencies", "DependenciesGui.exe"))
        utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "dependencies.exe"),
                         os.path.join(self.imageDir(), "dev-utils", "dependencies", "Dependencies.exe"))
        return True
