import info
from CraftConfig import *

class subinfo(info.infoclass):

    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "icons and bitmaps for the oxygen style"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


