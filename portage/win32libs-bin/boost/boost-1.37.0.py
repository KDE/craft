import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.37.0-1']:
            self.targets[ version ] = self.getPackage( repoUrl, "boost", version )

        ## @todo url's returned from self.getPackage are compiler specific, hard coded digests does not work yet
        #self.targetDigests['1.37.0-1-vc90'] = ['e789822568e9ed4e217d9f962e3388643ebda473',
        #                                       '66f29eff14ccdabdb4d5dfea1f722eea4fe8202d']            
        self.defaultTarget = '1.37.0-1'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
