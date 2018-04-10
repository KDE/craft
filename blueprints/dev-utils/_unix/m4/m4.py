import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["1.4.18"]:
            self.targets[ ver ] = f"https://ftp.gnu.org/gnu/m4/m4-{ver}.tar.xz"
            self.targetInstSrc[ ver ] = f"m4-{ver}"
            self.targetInstallPath[ver] = "dev-utils"

        self.targetDigests["1.4.18"] = (['f2c1e86ca0a404ff281631bdc8377638992744b175afb806e25871a24a934e07'], CraftHash.HashAlgorithm.SHA256)
        self.description = "GNU M4 is an implementation of the traditional Unix macro processor."
        self.defaultTarget = "1.4.18"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
