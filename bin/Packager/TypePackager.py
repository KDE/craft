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

    PackagerTypes = [ "SevenZipPackager", "KDEWinPackager", "MSIFragmentPackager",
                      "InnoSetupPackager", "NullsoftInstallerPackager" ]

    def __init__( self, defaultType = emergeSettings.get("Packager", "PackageType", "SevenZipPackager") ):
        EmergeDebug.debug("TypePackager __init__ %s" % defaultType, 2)
        PackagerBase.__init__(self)
        self.defaultPackager = defaultType
        self.packager = None
        self.changePackager(None)

    def changePackager(self, packagerName=None):
        if not packagerName == None and ("Packager", "PackageType") in emergeSettings:
            EmergeDebug.info("Packager setting %s overriten by with %s" % (packagerName, emergeSettings.get("Packager", "PackageType")))
            packagerName = emergeSettings.get("Packager", "PackageType")
        if packagerName == None: packagerName = self.defaultPackager

        package = None
        if packagerName == "SevenZipPackager":
            package = SevenZipPackager
        elif packagerName == "NullsoftInstallerPackager":
            package = NullsoftInstallerPackager
        elif packagerName == "KDEWinPackager":
            Tpackage  = KDEWinPackager
        elif packagerName == "MSIFragmentPackager":
            package = MSIFragmentPackager
        elif packagerName == "InnoSetupPackager":
            package = InnoSetupPackager
        else:
            """ the default !!! """
            package = SevenZipPackager
        if self.packager != package:
            self.packager = package
            TypePackager.__bases__ = ( self.packager, )
            self.packager.__init__( self, initialized = True )

    def createPackage( self ):
        return self.packager.createPackage( self )
