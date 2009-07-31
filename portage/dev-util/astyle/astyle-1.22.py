import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.22'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/astyle-1.22-bin.zip"
        self.targetMergePath['1.22'] = "dev-utils";
        self.defaultTarget = '1.22'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
