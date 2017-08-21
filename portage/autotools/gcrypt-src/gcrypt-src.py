import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["1.7.8"]:
            self.targets[ ver ] = f"ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"libgcrypt-{ver}"

        self.targetDigests['1.7.8'] = (['948276ea47e6ba0244f36a17b51dcdd52cfd1e664b0a1ac3bc82134fb6cec199'], CraftHash.HashAlgorithm.SHA256)
        self.shortDescription = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = "1.7.8"

    def setDependencies( self ):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["autotools/gpg-error-src"] = "default"

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )


    def install( self ):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
