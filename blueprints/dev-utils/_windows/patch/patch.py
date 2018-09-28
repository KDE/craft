import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['2.5.9'] = "http://downloads.sourceforge.net/sourceforge/gnuwin32/patch-2.5.9-7-bin.zip"
        self.targetInstallPath["2.5.9"] = "dev-utils"
        self.targetDigests['2.5.9'] = '7b2ec738881f4e962e54e0f330b67c42635266b7'
        self.defaultTarget = '2.5.9'

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
        manifest = os.path.join(self.packageDir(), "patch.exe.manifest")
        patch = os.path.join(self.installDir(), "bin", "patch.exe")
        return utils.embedManifest(patch, manifest)
