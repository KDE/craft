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

    def createPortablePackage(self) -> bool:
        """create portable 7z package with digest files located in the manifest subdir"""
        self.setupName = self.defines.get("setupname", os.path.join(self.packageDestinationDir(), self.binaryArchiveName(includeRevision=True)))

        if not os.path.isabs(self.setupName):
            absSetupPath = os.path.join(self.packageDestinationDir(), self.setupName)

        srcdir = self.defines.get("srcdir", self.archiveDir())

        return self._compress(self.setupName, srcdir, self.packageDestinationDir())

    def createPackage(self):
        """ create a package """

        if not self.internalCreatePackage():
          return False

        if not self.createPortablePackage():
          return False

        CraftHash.createDigestFiles(self.setupName)

        return True
