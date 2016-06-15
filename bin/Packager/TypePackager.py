#
# copyright (c) 2015 Patrick Spendrin <ps_ml@gmx.de>
#
import EmergeDebug
from Packager.PackagerBase import *

from Packager.KDEWinPackager import *
from Packager.SevenZipPackager import *
from Packager.MSIFragmentPackager import *
from Packager.InnoSetupPackager import *
from Packager.NullsoftInstallerPackager import *

class TypePackager( PackagerBase ):
    """packager that is used in place of different other packagers
The packager used can be decided at runtime
"""
    def __init__( self, defaultType = eval(emergeSettings.get("Packager", "PackageType", "SevenZipPackager")) ):
        EmergeDebug.debug("TypePackager __init__ %s" % defaultType, 2)
        PackagerBase.__init__(self)
        self.defaultPackager = defaultType
        self.__packager = None
        self.changePackager(None)

    def changePackager(self, packager=None):
        if not packager == None and ("Packager", "PackageType") in emergeSettings:
            EmergeDebug.info("Packager setting %s overriten by with %s" % (packager, emergeSettings.get("Packager", "PackageType")))
            packager = eval(emergeSettings.get("Packager", "PackageType"))
        if packager == None: packager = self.defaultPackager

        if self.__packager != packager:
            TypePackager.__bases__ = (packager,)
            TypePackager.__bases__[0].__init__(self, initialized=True)
            self.__packager = packager

    def createPackage( self ):
        return TypePackager.__bases__[0].createPackage(self)
