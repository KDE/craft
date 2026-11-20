import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "PatchELF is a simple utility for modifying existing ELF executables and libraries."
        self.releaseManagerId = 2598

        for ver in ["0.18.0", "0.19.3"]:
            self.targets[ver] = f"https://github.com/NixOS/patchelf/releases/download/{ver}/patchelf-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"patchelf-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["0.18.0"] = (["64de10e4c6b8b8379db7e87f58030f336ea747c0515f381132e810dbf84a86e7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.19.3"] = (["fac76a3c0b730e8d53ea1d10cd6015322d78c9900af91736f2cca51d5837b612"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.19.3"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # we are bootstrapping no gtk-doc etc yet
        self.subinfo.options.configure.autoreconf = False
