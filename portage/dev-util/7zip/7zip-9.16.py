import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['9.16'] = "http://downloads.sourceforge.net/sourceforge/sevenzip/7za916.zip"
        self.targetDigests['9.16'] = 'b389a6e2f93c18daae20393532af0e4e85ebe6f4'
        self.targetInstallPath['9.16'] = "bin"
        self.defaultTarget = '9.16'
    
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget']       = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
