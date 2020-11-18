import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['2.5.9'] = "http://downloads.sourceforge.net/sourceforge/gnuwin32/patch-2.5.9-7-bin.zip"
        self.targets['2.7.6'] = "https://files.kde.org/craft/3rdparty/patch/msys-patch-2.7.6.7z"
        self.targetInstallPath["2.5.9"] = "dev-utils"
        self.targetInstallPath["2.7.6"] = "dev-utils/patch"
        self.targetDigests['2.5.9'] = '7b2ec738881f4e962e54e0f330b67c42635266b7'
        self.targetDigests['2.7.6'] = (['2a8ed85190fab42861d64cdfd65015386ea82004e64df04b03eb9640429f9bcf'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '2.7.6'

    def setDependencies(self):
        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["dev-utils/uactools"] = None
        self.runtimeDependencies["virtual/bin-base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        if self.buildTarget == "2.5.9":
            manifest = os.path.join(self.packageDir(), "patch.exe.manifest")
            patch = os.path.join(self.installDir(), "bin", "patch.exe")
            return utils.embedManifest(patch, manifest)
        else:
            return utils.createShim(self.imageDir() / "bin/patch.exe", self.installDir() / "patch.exe")
