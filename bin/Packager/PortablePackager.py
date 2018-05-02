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

    def createPortablePackage(self) -> str:
        """create portable 7z package with digest files located in the manifest subdir"""
        setupname = self.defines.get("setupname", os.path.join(self.packageDestinationDir(), self.binaryArchiveName(includeRevision=True)))
        srcdir = self.defines.get("srcdir", self.archiveDir())

        if not self._compress(setupname, srcdir, self.packageDestinationDir()):
          return None
        return setupname

    def createPackage(self):
        """ create a package """

        if not self.internalCreatePackage():
          return False

        absSetupPath = self.createPortablePackage()

        if not os.path.isabs(absSetupPath):
            absSetupPath = os.path.join(self.packageDestinationDir(), absSetupPath)

        CraftHash.createDigestFiles(absSetupPath)

        return True
