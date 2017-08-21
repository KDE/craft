import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ["1.27"]:
            self.targets[ver] = f"ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgpg-error-{ver}"
        self.targetDigests['1.27'] = (['4f93aac6fecb7da2b92871bb9ee33032be6a87b174f54abf8ddf0911a22d29d2'], CraftHash.HashAlgorithm.SHA256)
        self.shortDescription = "Small library with error codes and descriptions shared by most GnuPG related software"
        self.defaultTarget = "1.27"

    def setDependencies( self ):
        self.buildDependencies["dev-util/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )

    def install( self ):
        if not AutoToolsPackageBase.install(self):
            return False
        return self.copyToMsvcImportLib()
