import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["2.4.6"]:
            self.targets[ ver ] = f"https://ftp.gnu.org/gnu/libtool/libtool-{ver}.tar.xz"
            self.targetInstSrc[ ver ] = f"libtool-{ver}"
            self.targetInstallPath[ver] = "dev-utils"

        #self.targetDigests["2.4.6"] = (['5d05bb38a23fd3312b10aea93840feec685bdf4a41146e78882848165d3ae921'], CraftHash.HashAlgorithm.SHA256)
        self.description = "GNU libtool is a generic library support script."
        self.defaultTarget = "2.4.6"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args += " --disable-static --enable-shared "

