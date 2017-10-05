#
# copyright (c) 2015 Patrick Spendrin <ps_ml@gmx.de>
#

from Packager.CreateArchivePackager import *
from Packager.InnoSetupPackager import *
from Packager.MacDMGPackager import *
from Packager.MSIFragmentPackager import *
from Packager.NullsoftInstallerPackager import *
from Packager.PortablePackager import *
from Packager.SevenZipPackager import *


class TypePackager(PackagerBase):
    """packager that is used in place of different other packagers
The packager used can be decided at runtime
"""

    def __init__(self, defaultType=eval(CraftCore.settings.get("Packager", "PackageType", "NullsoftInstallerPackager"))):
        CraftCore.log.debug("TypePackager __init__ %s" % defaultType)
        self.__packager = None
        self.changePackager(defaultType)

    def changePackager(self, packager=None):
        if not packager == None and ("Packager", "PackageType") in CraftCore.settings:
            CraftCore.log.debug(
                "Packager setting %s overriten by with %s" % (packager, CraftCore.settings.get("Packager", "PackageType")))
            packager = eval(CraftCore.settings.get("Packager", "PackageType"))

        if packager == None:
            return

        if self.__packager:
            bases = list(self.__class__.__bases__)
            for i in range(len(bases)):
                if bases[i] == self.__packager:
                    CraftCore.log.info(f"Replace Packager: {bases[i]} with {packager}")
                    bases[i] = packager
            self.__class__.__bases__ = tuple(bases)
        else:
            self.__class__.__bases__ += (packager,)
        packager.__init__(self)
        self.__packager = packager

    def createPackage(self):
        return self.__packager.createPackage(self)
