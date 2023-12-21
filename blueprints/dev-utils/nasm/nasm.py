import info
from CraftCompiler import CraftCompiler
from Package.AutoToolsPackageBase import *
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["2.13.03", "2.14.02", "2.15.05"]:
            if CraftCore.compiler.isMSVC():
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/win{CraftCore.compiler.bits}/nasm-{ver}-win{CraftCore.compiler.bits}.zip"
            else:
                self.targets[ver] = f"https://www.nasm.us/pub/nasm/releasebuilds/{ver}/nasm-{ver}.tar.bz2"

            self.targetInstSrc[ver] = f"nasm-{ver}"
            if CraftCore.compiler.isMSVC():
                self.targetInstallPath[ver] = os.path.join("dev-utils", "bin")
            else:
                self.targetInstallPath[ver] = "dev-utils"

        if CraftCore.compiler.isMSVC():
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
                self.targetDigests["2.14.02"] = (["18918ac906e29417b936466e7a2517068206c8db8c04b9762a5befa18bfea5f0"], CraftHash.HashAlgorithm.SHA256)
                self.targetDigests["2.15.05"] = (["f5c93c146f52b4f1664fa3ce6579f961a910e869ab0dae431bd871bdd2584ef2"], CraftHash.HashAlgorithm.SHA256)
            else:
                self.targetDigests["2.15.05"] = (["258c7d1076e435511cf2fdf94e2281eadbdb9e3003fd57f356f446e2bce3119e"], CraftHash.HashAlgorithm.SHA256)
        else:
            self.targetDigests["2.15.05"] = (["3c4b8339e5ab54b1bcb2316101f8985a5da50a3f9e504d43fa6f35668bee2fd0"], CraftHash.HashAlgorithm.SHA256)

        self.description = "This is NASM - the famous Netwide Assembler"
        self.webpage = "https://www.nasm.us/"
        self.defaultTarget = "2.15.05"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isMSVC():

    class Package(BinaryPackageBase):
        def __init__(self):
            BinaryPackageBase.__init__(self)

else:

    class Package(AutoToolsPackageBase):
        def __init__(self):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.autoreconf = False
