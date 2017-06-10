#
# copyright (c) 2015 Patrick Spendrin <ps_ml@gmx.de>
#
from CraftDebug import craftDebug
from Packager.PackagerBase import *

from Packager.SevenZipPackager import *
from Packager.MSIFragmentPackager import *
from Packager.InnoSetupPackager import *
from Packager.NullsoftInstallerPackager import *

class TypePackager( PackagerBase ):
    """packager that is used in place of different other packagers
The packager used can be decided at runtime
"""
    def __init__( self, defaultType = eval(craftSettings.get("Packager", "PackageType", "NullsoftInstallerPackager")) ):
        craftDebug.log.debug("TypePackager __init__ %s" % defaultType)
        PackagerBase.__init__(self)
        self.__packager = defaultType

    def changePackager(self, packager=None):
        if not packager == None and ("Packager", "PackageType") in craftSettings:
            craftDebug.log.debug("Packager setting %s overriten by with %s" % (packager, craftSettings.get("Packager", "PackageType")))
            packager = eval(craftSettings.get("Packager", "PackageType"))

        if packager == None:
            return

        self.__packager = packager

    def createPackage( self ):
        # slightly awkward: change base to the desired packager dynamically at runtime
        TypePackager.__bases__ = (self.__packager,)
        TypePackager.__bases__[0].__init__(self, initialized=True)

        return TypePackager.__bases__[0].createPackage(self)
