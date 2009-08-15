import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.65'] = "http://downloads.sourceforge.net/project/sevenzip/7-Zip/4.65/7za465.zip"
        self.targetInstallPath['4.65'] = "bin"
        self.defaultTarget = '4.65'
    
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
