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

    def createPortablePackage(self, packageSymbols) -> bool:
        """create portable 7z package with digest files located in the manifest subdir"""
        defines = self.setDefaults(self.defines)
        defines["setupname"] = str(Path(defines["setupname"]).with_suffix("." + CraftCore.settings.get("Packager", "7ZipArchiveType", "7z")))

        srcDir = defines.get("srcdir", self.archiveDir())

        if not self._compress(defines["setupname"], srcDir, self.packageDestinationDir()):
            return False
        CraftHash.createDigestFiles(defines["setupname"])

        if packageSymbols:
            dbgDir = f"{srcDir}-dbg"
            if os.path.exists(dbgDir):
                dbgName = "{0}-dbg{1}".format(*os.path.splitext(defines["setupname"]))
                if not self._compress(dbgName, dbgDir, self.packageDestinationDir()):
                    return False
                CraftHash.createDigestFiles(dbgName)
        return True

    def createPackage(self):
        """ create a package """

        packageSymbols = CraftCore.settings.getboolean("Packager", "PackageDebugSymbols", False)

        if not self.internalCreatePackage(seperateSymbolFiles=packageSymbols):
            return False

        return self.createPortablePackage(packageSymbols)
