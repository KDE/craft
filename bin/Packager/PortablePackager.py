#
# copyright (c) 2011 Hannah von Reth <vonreth@kde.org>
#
from .CollectionPackagerBase import *
from .SevenZipPackager import *
from .NullsoftInstallerPackager import *

class PortablePackager(CollectionPackagerBase, SevenZipPackager):
    """
Packager for portal 7zip archives
"""

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        SevenZipPackager.__init__(self)
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def createPortablePackage(self):
        """create portable 7z package with digest files located in the manifest subdir"""

        if CraftCore.compiler.isMSVC2017() and self.buildType() != "Debug":
            redistInstalelr = NullsoftInstallerPackager.getVCRedistLocation()
            redistDir = os.path.join(os.path.dirname(redistInstalelr), CraftCore.compiler.architecture,
                                    f"Microsoft.VC{CraftCore.compiler.getMsvcPlatformToolset()}.CRT")
            dest = os.path.join(self.archiveDir(), "bin") if  os.path.isdir(os.path.join(self.archiveDir(), "bin")) else self.archiveDir()
            utils.copyDir(redistDir, dest, linkOnly=False)

        if not "setupname" in self.defines or not self.defines["setupname"]:
            self.defines["setupname"] = os.path.join(self.packageDestinationDir(), self.binaryArchiveName(includeRevision=True))
        if not "srcdir" in self.defines or not self.defines["srcdir"]:
            self.defines["srcdir"] = self.archiveDir()

        self._compress(self.defines["setupname"], self.defines["srcdir"], self.packageDestinationDir())

    def createPackage(self):
        """ create a package """
        print("packaging using the PortablePackager")

        self.internalCreatePackage()
        self.createPortablePackage()
        CraftHash.createDigestFiles(self.defines["setupname"])
        return True
