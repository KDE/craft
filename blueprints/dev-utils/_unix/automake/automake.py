import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["1.16.1"]:
            self.targets[ ver ] = f"https://ftp.gnu.org/gnu/automake/automake-{ver}.tar.xz"
            self.targetInstSrc[ ver ] = f"automake-{ver}"
            self.targetInstallPath[ver] = "dev-utils"

        self.targetDigests["1.16.1"] = (['5d05bb38a23fd3312b10aea93840feec685bdf4a41146e78882848165d3ae921'], CraftHash.HashAlgorithm.SHA256)
        self.description = "Automake is a tool for automatically generating Makefile.in files compliant with the GNU Coding Standards."
        self.defaultTarget = "1.16.1"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-utils/autoconf"] = "default"

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args += " --disable-static --enable-shared "

