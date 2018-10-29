import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ["2.69"]:
            self.targets[ ver ] = f"https://ftp.gnu.org/gnu/autoconf/autoconf-{ver}.tar.xz"
            self.targetInstSrc[ ver ] = f"autoconf-{ver}"
            self.targetInstallPath[ver] = "dev-utils"

        self.targetDigests["2.69"] = (['64ebcec9f8ac5b2487125a86a7760d2591ac9e1d3dbd59489633f9de62a57684'], CraftHash.HashAlgorithm.SHA256)
        self.description = "Autoconf is an extensible package of M4 macros that produce shell scripts to automatically configure software source code packages."
        self.defaultTarget = "2.69"

    def setDependencies( self ):
        self.buildDependencies["dev-utils/m4"] = None

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared "

    def postInstall(self):
        for f in ["dev-utils/share/autoconf/autoconf/autoconf.m4f",
                  "dev-utils/share/autoconf/autotest/autotest.m4f",
                  "dev-utils/share/autoconf/m4sugar/m4sh.m4f",
                  "dev-utils/share/autoconf/m4sugar/m4sugar.m4f"]:
            if not utils.deleteFile(os.path.join(self.imageDir(), f)):
                return False
        return self.patchInstallPrefix([os.path.join(self.imageDir(), x) for x in ["dev-utils/bin/autoconf",
                                                                                   "dev-utils/bin/autoheader",
                                                                                   "dev-utils/bin/autom4te",
                                                                                   "dev-utils/bin/autoreconf",
                                                                                   "dev-utils/bin/autoscan",
                                                                                   "dev-utils/bin/autoupdate",
                                                                                   "dev-utils/bin/ifnames",
                                                                                   "dev-utils/share/autoconf/autom4te.cfg"]],
                                       self.subinfo.buildPrefix,
                                       CraftCore.standardDirs.craftRoot())

