import info
from Package import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ "gitHEAD" ] = "[git]kde:craft"
        self.defaultTarget = "gitHEAD"


    def setDependencies( self ):
        self.buildDependencies['dev-utils/git'] = 'default'


from Package.SourceOnlyPackageBase import *

class Package(SourceOnlyPackageBase, GitSource):
    def __init__( self):
        SourceOnlyPackageBase.__init__(self)
        GitSource.__init__(self,subinfo=self.subinfo)

    def checkoutDir(self):
        return os.path.join(CraftStandardDirs.craftBin(), "..")

    def fetch(self):
        GitSource.fetch(self)