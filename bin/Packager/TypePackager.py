#
# copyright (c) 2015 Patrick Spendrin <ps_ml@gmx.de>
#
import EmergeDebug
from Packager.PackagerBase import *

from Packager.KDEWinPackager import *
from Packager.SevenZipPackager import *
from Packager.MSIFragmentPackager import *
from Packager.InnoSetupPackager import *

class TypePackager( PackagerBase ):
    """packager that is used in place of different other packagers
The packager used can be decided at runtime
"""

    PackagerTypes = [ "SevenZipPackager", "KDEWinPackager", "MSIFragmentPackager", "InnoSetupPackager" ]

    def __init__( self, defaultType = "SevenZipPackager" ):
        EmergeDebug.debug("TypePackager __init__ %s" % defaultType, 2)
        self.defaultPackager = defaultType
        self.changePackager()

    def changePackager( self, packager=None ):
        if packager == None: packager = self.defaultPackager
        if packager == "SevenZipPackager":
            TypePackager.__bases__ = ( SevenZipPackager, )
        elif packager == "KDEWinPackager":
            TypePackager.__bases__ = ( KDEWinPackager, )
        elif packager == "MSIFragmentPackager":
            TypePackager.__bases__ = ( MSIFragmentPackager, )
        elif packager == "InnoSetupPackager":
            TypePackager.__bases__ = ( InnoSetupPackager, )
        else:
            """ the default !!! """
            TypePackager.__bases__ = ( SevenZipPackager, )
        TypePackager.__bases__[ 0 ].__init__( self, True )

    def createPackage( self ):
        return TypePackager.__bases__[ 0 ].createPackage( self )
