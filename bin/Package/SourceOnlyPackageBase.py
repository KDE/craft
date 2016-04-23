from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.BuildSystemBase import *
from Packager.PackagerBase import *


class SourceOnlyPackageBase( PackageBase, MultiSource, BuildSystemBase, PackagerBase ):
    """provides a base class for source dependency packages"""
    def __init__( self ):
        EmergeDebug.debug("SourceOnlyPackageBase.__init__ called", 2)
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        BuildSystemBase.__init__(self, "")
        PackagerBase.__init__(self)

# from BuildSystemBase:
    def configure( self ):
        return True

    def install( self ):
        return True

    def uninstall( self ):
        return True

    def runTests( self ):
        return True

    def make( self ):
        return True

# from PackagerBase:
    def createPackage( self ):
        return True