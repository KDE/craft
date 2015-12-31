#
# copyright (c) 2011 Hannah von Reth <vonreth@kde.org>
#
import EmergeDebug
import utils
from .CollectionPackagerBase import *
from .SevenZipPackager import *

class PortablePackagerList( PackagerLists ):
    """ dummy name for PackagerLists """

class PortablePackager( CollectionPackagerBase, SevenZipPackager ):
    """
Packager for portal 7zip archives
"""
    def __init__( self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__( self, whitelists, blacklists )
        SevenZipPackager.__init__(self)


    def createPortablePackage( self ):
        """create portable 7z package with digest files located in the manifest subdir"""

        if not self.packagerExe:
            EmergeDebug.die("could not find 7za in your path!")


        if not "setupname" in self.defines or not self.defines[ "setupname" ]:
            self.defines[ "setupname" ] = self._archiveName("")
        if not "srcdir" in self.defines or not self.defines[ "srcdir" ]:
            self.defines[ "srcdir" ] = self.imageDir()
            

        self._compress(self.defines[ "setupname" ], self.defines[ "srcdir" ], self.packageDestinationDir())

    def createPackage( self ):
        """ create a package """
        print("packaging using the PortablePackager")
        
        self.internalCreatePackage()

        self.createPortablePackage()
        utils.createDigestFile( os.path.join(self.packageDestinationDir(), self.defines[ "setupname" ]))
        return True
