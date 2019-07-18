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

    def createPortablePackage(self, defines) -> bool:
        """create portable 7z package with digest files located in the manifest subdir"""

        defines["setupname"] = str(Path(defines["setupname"]).with_suffix("." + CraftCore.settings.get("Packager", "7ZipArchiveType", "7z")))

        srcDir = defines.get("srcdir", self.archiveDir())

        return self._createArchive(defines["setupname"], srcDir, self.packageDestinationDir())

    def createPackage(self):
        """ create a package """

        defines = self.setDefaults(self.defines)
        if not self.internalCreatePackage(defines, True):
            return False

        return self.createPortablePackage(defines)
