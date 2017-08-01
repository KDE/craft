import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        arch = "32"
        if craftCompiler.isX64():
            arch = "64"
        for ver in ["1.7.8"]:
            self.targets[ ver ] = f"https://files.kde.org/craft/3rdparty/gpgme/mingw_{arch}/gcc/Release/gcrypt-src-{ver}-windows-mingw_{arch}-gcc.7z"
            #self.targetDigestUrls[ ver ] = f"http://files.kde.org/craft/3rdparty/gpgme/gcrypt-src-{compiler.architecture()}-{ver}-mingw-w64.7z.sha256"


        self.shortDescription = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = '1.7.8'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if craftCompiler.isGCCLike():
            self.runtimeDependencies["autotools/gcrypt-src"] = "default"
        else:
            self.runtimeDependencies["win32libs/mingw-crt4msvc"] = "default"
            self.runtimeDependencies["win32libs/gpg-error"] = "default"

from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *

class BinPackage(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)

class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, not craftCompiler.isGCCLike(), classA=BinPackage)
