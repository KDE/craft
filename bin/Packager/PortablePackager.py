#
# copyright (c) 2011 Hannah von Reth <vonreth@kde.org>
#
from CraftDebug import craftDebug
import CraftHash
import utils
from .CollectionPackagerBase import *
from .SevenZipPackager import *

class PortablePackager( CollectionPackagerBase, SevenZipPackager ):
    """
Packager for portal 7zip archives
"""
    def __init__( self, whitelists=None, blacklists=None, initialized=False):
        SevenZipPackager.__init__(self, initialized=initialized)
        CollectionPackagerBase.__init__( self, whitelists, blacklists, initialized=initialized )


    def createPortablePackage( self ):
        """create portable 7z package with digest files located in the manifest subdir"""
        if not "setupname" in self.defines or not self.defines[ "setupname" ]:
            self.defines[ "setupname" ] = self.binaryArchiveName("")
        if not "srcdir" in self.defines or not self.defines[ "srcdir" ]:
            self.defines[ "srcdir" ] = self.archiveDir()
            

        self._compress(self.defines[ "setupname" ], self.defines[ "srcdir" ], self.packageDestinationDir())

    def createPackage( self ):
        """ create a package """
        print("packaging using the PortablePackager")
        
        self.internalCreatePackage()

        self.createPortablePackage()
        CraftHash.createDigestFiles(os.path.join(self.packageDestinationDir(), self.defines["setupname"]))
        return True
