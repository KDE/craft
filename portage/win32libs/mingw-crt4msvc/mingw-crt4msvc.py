import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["5.4.0"]:
            self.targets[ ver ] = f"http://files.kde.org/craft/3rdparty/gpgme/runtime-{craftCompiler.architecture()}-{ver}-mingw-w64.7z"
            #self.targetDigestUrls[ ver ] = f"http://files.kde.org/craft/3rdparty/gpgme/runtime-{compiler.architecture()}-{ver}-mingw-w64.7z.sha256"


        self.shortDescription = "The crt for mingw compiled binaries"
        self.defaultTarget = '5.4.0'

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
