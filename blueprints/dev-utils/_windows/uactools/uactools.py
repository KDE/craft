# uactools : Binary package of the tools to handle UAC from kde-windows.
# mt.exe can be used to embed manifest files to disable heuristic UAC raise
# requests, setuac.exe can be used to enable raise the privileges of a program.
# The according source package is uactools-pkg


import info
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.GCCLike

    def setTargets(self):
        latest = "20100711"
        self.targets[latest] = f"http://downloads.sourceforge.net/kde-windows/uactools-mingw4-{latest}-bin.tar.bz2"
        self.targetDigests[latest] = "b59ab7ac9190cbfe5b00acae05f909ea8f22bd3a"
        self.targetInstallPath[latest] = "dev-utils"
        self.defaultTarget = latest

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
