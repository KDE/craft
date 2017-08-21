import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["7.1.0"]:
            self.targets[ ver ] = f"https://files.kde.org/craft/3rdparty/gpgme/mingw_{craftCompiler.bits}/gcc/Release/runtime-{ver}-windows-mingw_{craftCompiler.bits}-gcc.7z"
            self.targetDigestUrls[ver] = f"{self.targets[ver]}.sha256"


        self.shortDescription = "The crt for mingw compiled binaries"
        self.defaultTarget = "7.1.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *

class BinPackage(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)

class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, not craftCompiler.isGCCLike(), classA=BinPackage)
