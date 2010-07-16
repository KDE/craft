import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.0.3'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/upx-3.0.3-bin.zip"
        self.targetDigests['3.0.3'] = '6cbceca56b8c83b23e9665f8ba8b14e73aefa58d'
        self.defaultTarget = '3.0.3'
    
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
