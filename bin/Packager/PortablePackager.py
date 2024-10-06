#
# copyright (c) 2011 Hannah von Reth <vonreth@kde.org>
#
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftBase import InitGuard

from .CollectionPackagerBase import CollectionPackagerBase
from .SevenZipPackager import SevenZipPackager


class PortablePackager(CollectionPackagerBase, SevenZipPackager):
    """Packager for portal 7zip archives"""

    @InitGuard.init_once
    def __init__(self, package: CraftPackageObject, whitelists=None, blacklists=None):
        SevenZipPackager.__init__(self, package)
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def setDefaults(self, defines: set[str, str]) -> set[str, str]:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}{self.archiveExtension}"
        return defines

    def createPortablePackage(self, defines) -> bool:
        """create portable 7z package with digest files located in the manifest subdir"""
        return self._createArchive(
            defines["setupname"],
            defines.get("srcdir", self.archiveDir()),
            self.packageDestinationDir(),
        )

    def createPackage(self):
        """create a package"""

        defines = self.setDefaults(self.defines)
        if not self.internalCreatePackage(defines):
            return False

        return self.createPortablePackage(defines)
