import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.7"]:
            self.targets[ver] = f"https://github.com/lucasg/Dependencies/releases/download/v{ver}/Dependencies.zip"
            self.archiveNames[ver] = f"dependencies-{ver}.zip"
            self.targetInstallPath[ver] = "dev-utils/dependencies/"

        self.targetDigests["1.5"] = (['8d2dbc6e92ff22697d38675d1409a61e2971e05f3efe77be1eb48b035eff153d'], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://github.com/lucasg/Dependencies"
        self.description = "A rewrite of the old legacy software \"depends.exe\" in C# for Windows devs to troubleshoot dll load dependencies issues."
        self.defaultTarget = "1.7"


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
