import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.18.0"]:
            self.targets[ver] = f"https://github.com/NixOS/patchelf/releases/download/{ver}/patchelf-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"patchelf-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["0.18.0"] = (["64de10e4c6b8b8379db7e87f58030f336ea747c0515f381132e810dbf84a86e7"], CraftHash.HashAlgorithm.SHA256)
        self.description = "PatchELF is a simple utility for modifying existing ELF executables and libraries."
        self.defaultTarget = "0.18.0"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # we are bootstrapping no gtk-doc etc yet
        self.subinfo.options.configure.autoreconf = False
