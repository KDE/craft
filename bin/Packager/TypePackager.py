#
# copyright (c) 2015 Patrick Spendrin <ps_ml@gmx.de>
#
from CraftDebug import craftDebug
from Packager.PackagerBase import *

from Packager.InnoSetupPackager import *
from Packager.MSIFragmentPackager import *
from Packager.NullsoftInstallerPackager import *
from Packager.PortablePackager import *
from Packager.SevenZipPackager import *

class TypePackager( PackagerBase ):
    """packager that is used in place of different other packagers
The packager used can be decided at runtime
"""
    def __init__( self, defaultType = eval(craftSettings.get("Packager", "PackageType", "NullsoftInstallerPackager")) ):
        craftDebug.log.debug("TypePackager __init__ %s" % defaultType)
        self.__packager = None
        self.changePackager(defaultType)

    def changePackager(self, packager=None):
        if not packager == None and ("Packager", "PackageType") in craftSettings:
            craftDebug.log.debug("Packager setting %s overriten by with %s" % (packager, craftSettings.get("Packager", "PackageType")))
            packager = eval(craftSettings.get("Packager", "PackageType"))

        if packager == None:
            return

        if self.__packager:
            bases = list(self.__class__.__bases__)
            for i in range(len(bases)):
                if bases[i] == self.__packager:
                    craftDebug.log.info(f"Replace Packager: {bases[i]} with {packager}")
                    bases[i] = packager
            self.__class__.__bases__ = tuple(bases)
        else:
            self.__class__.__bases__ += (packager,)
        packager.__init__(self, self.__packager is not None)
        self.__packager = packager

    def createPackage(self):
        return self.__packager.createPackage(self)

