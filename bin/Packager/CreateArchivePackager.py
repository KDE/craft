from Packager.CollectionPackagerBase import *

class CreateArchivePackager(CollectionPackagerBase):
    """@brief Simple packager for testing what contents an archive would have

    This packager collects everything and puts into the archive dir of the resp. package"""

    @InitGuard.init_once
    def __init__( self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def createPackage( self ):
        """ create a package """
        CraftCore.log.debug("packaging using the CreateArchivePackager")

        defines = self.setDefaults(self.defines)
        return self.internalCreatePackage(defines, seperateSymbolFiles=True)
