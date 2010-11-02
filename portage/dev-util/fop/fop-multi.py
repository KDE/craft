import info
import platform

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.0'] = 'http://apache.parentingamerica.com/xmlgraphics/fop/binaries/fop-1.0-bin.zip'
        self.targetDigests['1.0'] = 'afef3bbfed5543c92bc9ed2d7651422580f98bd9'
        self.targetMergeSourcePath['1.0'] = 'fop-1.0'
        self.defaultTarget = '1.0'
            
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        ## @todo manifest files are also written in dev-utils/bin - fix this 
        self.subinfo.options.merge.destinationPath = "dev-utils/bin"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
