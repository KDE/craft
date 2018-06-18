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
        self.setupName = None

    def createPortablePackage(self, packageSymbols) -> bool:
        """create portable 7z package with digest files located in the manifest subdir"""
        self.setupName = self.defines.get("setupname", os.path.join(self.packageDestinationDir(), self.binaryArchiveName(includeRevision=True)))

        srcDir = self.defines.get("srcdir", self.archiveDir())

        if not self._compress(self.setupName, srcDir, self.packageDestinationDir()):
            return False
        CraftHash.createDigestFiles(self.setupName)

        if packageSymbols:
            dbgDir = f"{srcDir}-dbg"
            if os.path.exists(dbgDir):
                dbgName = "{0}-dbg{1}".format(*os.path.splitext(self.setupName))
                if not self._compress(dbgName, dbgDir, self.packageDestinationDir()):
                    return False
                CraftHash.createDigestFiles(dbgName)
        return True

    def createPackage(self):
        """ create a package """

        packageSymbols = CraftCore.settings.get("Packager", "PackageDebugSymbols", False)

        if not self.internalCreatePackage(seperateSymbolFiles=packageSymbols):
            return False

        return self.createPortablePackage(packageSymbols)
