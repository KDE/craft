import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["1.9.0"]:
            self.targets[ver] = f"ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"gpgme-{ver}"

        self.targetDigests["1.9.0"] = (["1b29fedb8bfad775e70eafac5b0590621683b2d9869db994568e6401f4034ceb"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.9.0"] = [("gpgme-1.9.0-20170801.diff", 1)]

        self.shortDescription = "GnuPG cryptography support library (runtime)"
        self.defaultTarget = "1.9.0"

    def setDependencies( self ):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["autotools/gpg-error-src"] = "default"
        self.runtimeDependencies["autotools/assuan2-src"] = "default"

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args = "--enable-languages=no"

    def install(self):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
