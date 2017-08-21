import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["2.4.3"]:
            self.targets[ ver ] = f"ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = f"libassuan-{ver}"

        self.targetDigests['2.4.3'] = (['22843a3bdb256f59be49842abf24da76700354293a066d82ade8134bb5aa2b71'], CraftHash.HashAlgorithm.SHA256)

        self.shortDescription = "An IPC library used by some of the other GnuPG related packages"
        self.defaultTarget = "2.4.3"

    def setDependencies( self ):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["autotools/gpg-error-src"] = "default"

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )

    def install( self ):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
