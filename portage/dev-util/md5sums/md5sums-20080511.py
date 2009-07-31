import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['20080511'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/md5sums-20080511-bin.zip"
        self.defaultTarget = '20080511'
        self.targetMergePath['20080511'] = "dev-utils";
    
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
