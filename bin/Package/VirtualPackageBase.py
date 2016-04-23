from Package.SourceOnlyPackageBase import *
import portage


class VirtualPackageBase( SourceOnlyPackageBase):
    """provides a base class for virtual packages"""
    def __init__( self ):
        EmergeDebug.debug("VirtualPackageBase.__init__ called", 2)
        SourceOnlyPackageBase.__init__( self )

# from SourceBase:
    def fetch( self, dummyRepoSource=None):
        return True

    def unpack( self ):
        return True

    def createPatch( self ):
        return True

    def getUrls( self ):
        return True

    def repositoryUrl( self, dummyIndex=0 ):
        return ""

    def repositoryUrlCount( self ):
        return 0

    def localFileNamesBase( self ):
        return []


# from PackagerBase:
    def createPackage( self ):
        for dep in self.subinfo.dependencies:
            category,package = dep.split( "/" )
            if not portage.getPackageInstance(category,package).createPackage():
                return False
        return True
