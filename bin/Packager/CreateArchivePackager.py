from CraftBase import InitGuard
from CraftCore import CraftCore
from Packager.CollectionPackagerBase import CollectionPackagerBase


class CreateArchivePackager(CollectionPackagerBase):
    """@brief Simple packager for testing what contents an archive would have

    This packager collects everything and puts into the archive dir of the resp. package"""

    @InitGuard.init_once
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        """create a package"""
        CraftCore.log.debug("packaging using the CreateArchivePackager")

        defines = self.setDefaults(self.defines)
        return self.internalCreatePackage(defines)
