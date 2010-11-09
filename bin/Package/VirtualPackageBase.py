from PackageBase import *;
from Source.SourceBase import *;
from BuildSystem.BuildSystemBase import *;
from Packager.PackagerBase import *;

class VirtualPackageBase( PackageBase, SourceBase, BuildSystemBase, PackagerBase ):
    """provides a base class for virtual packages"""
    def __init__( self ):
        utils.debug( "VirtualPackageBase.__init__ called", 2 )
        PackageBase.__init__( self )
        SourceBase.__init__( self )
        BuildSystemBase.__init__( self, "" )
        PackagerBase.__init__( self )

# from SourceBase:
    def fetch( self ): 
        return True

    def unpack( self ): 
        return True

    def createPatch( self ):
        return True

    def repositoryUrl( self, index=0 ):
        return ""

    def repositoryUrlCount( self ):
        return 0

    def localFileNamesBase( self ):
        return []

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
            
    def dumpDependencies( self ):
        return True
        
# from PackagerBase:
    def createPackage( self ):
        return True
