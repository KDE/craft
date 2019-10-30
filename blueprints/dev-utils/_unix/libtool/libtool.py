import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["2.4.6"]:
            self.targets[ ver ] = f"https://ftp.gnu.org/gnu/libtool/libtool-{ver}.tar.xz"
            self.targetInstSrc[ ver ] = f"libtool-{ver}"
            self.targetInstallPath[ver] = "dev-utils"

        self.targetDigests["2.4.6"] = (['7c87a8c2c8c0fc9cd5019e402bed4292462d00a718a7cd5f11218153bf28b26f'], CraftHash.HashAlgorithm.SHA256)
        self.description = "GNU libtool is a generic library support script."
        self.patchLevel["2.4.6"] = 1
        self.defaultTarget = "2.4.6"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/automake"] = None

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += " --program-prefix=g"


    def postInstall(self):
        tool = "libtool"
        if CraftCore.compiler.isMacOS:
            tool = f"g{tool}"
        return self.patchInstallPrefix([os.path.join(self.imageDir(), x) for x in [f"dev-utils/bin/{tool}",
                                                                                   f"dev-utils/bin/{tool}ize"]],
                                       self.subinfo.buildPrefix,
                                       CraftCore.standardDirs.craftRoot())

